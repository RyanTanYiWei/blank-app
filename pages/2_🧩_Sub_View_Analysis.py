import streamlit as st
from pathlib import Path
import tempfile
from typing import Dict, List, Set, Tuple
import re
import pandas as pd
import pysd
import time

if "timings" not in st.session_state:
    st.session_state.timings = {}


st.set_page_config(layout="wide", page_title="View Connections", page_icon="🧩")

# Path to CSS file
css_file = Path(__file__).parent.parent / "assets" / "style.css"

if css_file.exists():
    css_content = css_file.read_text()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

st.title("🧩 Sub Model Analysis")
st.caption("Built for Modellers with Many the What-Connects-to-Where Questions")
st.warning(
    "⚠️ This tool assumes that each **view** in your Vensim model represents a **submodel**. "
)

st.markdown("""
Upload a `.mdl` file. This tool will shows  
🔹 Split variables by model views  
🔹 Display an interactive network of connections between views  
🔹 List variables from one view are used in formulas of another  
🔹 Download view-to-view matrix and shared variables as CSV  
""")

# --- File upload ---
file = st.file_uploader("Vensim model (.mdl)", type=["mdl"])

# Detect if a new file is uploaded and clear previous session state
if file:
    if "uploaded_file_name" not in st.session_state or st.session_state.uploaded_file_name != file.name:
        # New file, reset session state
        keys_to_clear = [
            "df_merged", "debug", "view_vars", "var_formula",
            "connections", "view_matrix", "timings",
            "view_a", "view_b"
        ]
        for k in keys_to_clear:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state.uploaded_file_name = file.name

# --- Utility ---
def save_to_temp(uploaded_file) -> Path:
    if not uploaded_file:
        return None
    tmp_dir = Path(tempfile.mkdtemp(prefix="vensim_"))
    tmp_path = tmp_dir / Path(uploaded_file.name).name
    tmp_path.write_bytes(uploaded_file.read())
    return tmp_path

# --- Extraction (raw variables) ---
def extract_raw_variables(path: Path) -> Tuple[pd.DataFrame, List[str]]:
    from pysd.translators.vensim.vensim_file import VensimFile
    debug = []

    vf = VensimFile(str(path))
    vf.parse()
    sections = getattr(vf, "sections", []) or []
    debug.append(f"Raw parse sections: {len(sections)}")

    def _stringify_equation(obj):
        for attr in ["rhs","equation","expr","expression","raw_equation","raw","text","value","definition"]:
            val = getattr(obj, attr, None)
            if val is not None:
                return str(val)
        comp = getattr(obj, "component", None)
        if comp:
            return _stringify_equation(comp)
        try:
            return str(obj)
        except Exception:
            return None

    raw_vars = []
    for section in sections:
        section_name = getattr(section, "name", None) or "Unknown Section"
        elements = getattr(section, "elements", []) or []
        debug.append(f"Section '{section_name}' elements: {len(elements)}")
        for element in elements:
            comps = getattr(element, "components", None)
            if comps:
                if isinstance(comps, dict):
                    for name, comp in comps.items():
                        eq = _stringify_equation(comp)
                        raw_vars.append({"Variable": name, "Section": section_name, "Formula": eq})
                elif isinstance(comps, list):
                    for comp in comps:
                        name = getattr(comp, "name", None)
                        eq = _stringify_equation(comp)
                        raw_vars.append({"Variable": name, "Section": section_name, "Formula": eq})
            else:
                name = getattr(element, "name", None)
                eq = _stringify_equation(element)
                raw_vars.append({"Variable": name, "Section": section_name, "Formula": eq})

    df_raw = pd.DataFrame(raw_vars)
    debug.append(f"Raw variables parsed: {len(df_raw)}")
    return df_raw, debug

# --- PySD views parsing ---
def parse_views_pysd(path: Path, debug: List[str]) -> pd.DataFrame:
    """
    Parse views from a Vensim model using PySD, cleaning problematic coordinate text.
    Skips variables that PySD cannot parse and returns a DataFrame mapping Variable -> View.
    """
    df_views = pd.DataFrame(columns=["Variable", "View"])
    
    try:
        # Read and clean the .mdl text in memory (no writing to disk)
        text = path.read_text()
        cleaned_text = re.sub(r"\(\d+,\d+\)\|", "", text)
        
        # PySD allows reading from a string via a temporary file-like object
        import io
        tmp_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".mdl", delete=False)
        tmp_file.write(cleaned_text)
        tmp_file.flush()
        
        models = pysd.read_vensim(tmp_file.name, split_views=True, initialize=False)
        tmp_file.close()
        
        # Map PySD variable names back to Vensim names
        py_to_vensim = {py_name: vensim_name for vensim_name, py_name in models.namespace.items()}
        
        # Detect variables PySD cannot parse
        failed_vars = []
        for py_var, obj in getattr(models, "_namespace", {}).items():
            try:
                _ = getattr(obj, "equation", getattr(obj, "rhs", None))
            except Exception:
                failed_vars.append(py_var)
        
        # Build the view mapping, skipping failed variables
        view_mapping = []
        for view_name, py_vars in getattr(models, "modules", {}).items():
            for py_var in py_vars:
                if py_var in failed_vars:
                    continue
                vensim_name = py_to_vensim.get(py_var, py_var)
                view_mapping.append({"Variable": vensim_name, "View": view_name})
        
        if view_mapping:
            df_views = pd.DataFrame(view_mapping)
        
        if failed_vars:
            debug.append(f"⚠️ PySD could not parse {len(failed_vars)} variables: {failed_vars[:10]} ...")
        
        debug.append(f"Views parsed: {len(df_views)} variables across {len(getattr(models,'modules',{}))} views")
    
    except Exception as e:
        debug.append(f"PySD parsing failed: {e}")
    
    return df_views


# --- Compute connections ---
def compute_view_connections(view_vars: Dict[str, List[str]], var_formula: Dict[str, str]) -> Dict[Tuple[str,str], Set[str]]:
    connections: Dict[Tuple[str,str], Set[str]] = {}
    var_pattern = {v: re.compile(r'\b' + re.escape(v) + r'\b') for v in var_formula.keys()}
    for view_to, vars_to in view_vars.items():
        for view_from, vars_from in view_vars.items():
            if view_to == view_from:
                continue
            shared_vars = set()
            for vf in vars_from:
                pattern = var_pattern.get(vf)
                if not pattern:
                    continue
                for vt in vars_to:
                    if pattern.search(var_formula.get(vt, "")):
                        shared_vars.add(vf)
            if shared_vars:
                connections[(view_from, view_to)] = shared_vars
    return connections

# --- Generate matrix ---
def generate_view_matrix(view_vars: Dict[str, List[str]], var_formula: Dict[str, str]) -> pd.DataFrame:
    views_sorted = sorted(view_vars.keys())
    matrix_data = {}
    for src in views_sorted:
        row = {}
        for tgt in views_sorted:
            if src == tgt:
                row[tgt] = ""
                continue
            used_vars = set()
            for v in view_vars[src]:
                pattern = re.compile(r'\b' + re.escape(v) + r'\b')
                for t_var in view_vars[tgt]:
                    if pattern.search(var_formula.get(t_var, "")):
                        used_vars.add(v)
            row[tgt] = ", ".join(sorted(used_vars)) if used_vars else ""
        matrix_data[src] = row
    return pd.DataFrame.from_dict(matrix_data, orient="index")

# --- Network ---
# --- Network ---
def plot_network(connections: Dict[Tuple[str,str], Set[str]]):
    try:
        from pyvis.network import Network
        import streamlit.components.v1 as components
        import tempfile
        from pathlib import Path
        import math
    except Exception as e:
        st.warning(f"Visualization libraries not available: {e}")
        return

    net_height = 450
    net = Network(height=f"{net_height}px", width="100%", notebook=False, directed=True, bgcolor="#ffffff", font_color="black")

    # Compute node degrees for sizing
    node_degree = {}
    for (src, tgt), vars_set in connections.items():
        node_degree[src] = node_degree.get(src, 0) + len(vars_set)
        node_degree[tgt] = node_degree.get(tgt, 0) + len(vars_set)

    max_degree = max(node_degree.values()) if node_degree else 1
    min_degree = min(node_degree.values()) if node_degree else 0

    all_nodes = sorted(set([v for pair in connections.keys() for v in pair]))

    # Layout selection
    layout_choice = st.selectbox("Network Layout", ["Force-Directed", "Circular"], index=0)

    # Add nodes
    if layout_choice == "Circular":
        n = len(all_nodes)
        radius = 150 + 5 * n  # Scale radius with number of nodes
        for i, node in enumerate(all_nodes):
            angle = 2 * math.pi * i / max(1, n)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            degree = node_degree.get(node, 0)
            size = 8 + (degree - min_degree) / max(1, max_degree - min_degree) * 12
            net.add_node(
                node,
                label=node,
                title=f"{node} ({degree} shared vars)",
                size=size,
                x=x,
                y=y,
                physics=False,
                color={
                    "border": "#2e86de",
                    "background": "#97c2fc",
                    "highlight": {"background": "red", "border": "darkred"}
                }
            )
    else:
        for node in all_nodes:
            degree = node_degree.get(node, 0)
            size = 12 + (degree - min_degree) / max(1, max_degree - min_degree) * 30
            net.add_node(
                node,
                label=node,
                title=f"{node} ({degree} shared vars)",
                size=size,
                color={
                    "border": "#2e86de",
                    "background": "#97c2fc",
                    "highlight": {"background": "red", "border": "darkred"}
                }
            )

    # Add edges: only inflows will highlight when target node is clicked
    for (src, tgt), vars_set in connections.items():
        width = max(1, min(10, len(vars_set)))
        net.add_edge(
            src, tgt,
            value=len(vars_set),
            title=f"{len(vars_set)} shared vars",
            width=width,
            smooth={"enabled": True, "type": "curvedCW"},
            color={
                "color": "#848484",          # default
                "highlight": "red",          # highlighted edges (inflows)
                "hover": "orange"
            }
        )

    # Apply physics only if force-directed
    if layout_choice == "Force-Directed":
        net.barnes_hut(
            gravity=-8000,
            central_gravity=0.2,
            spring_length=200,
            spring_strength=0.08,
            damping=0.4,
            overlap=0
        )
        net.toggle_physics(True)
    else:
        net.toggle_physics(False)

    # Show physics buttons below
    net.show_buttons(filter_=['physics'])

    # Render in Streamlit
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp_file.name)
    components.html(Path(tmp_file.name).read_text(), height=net_height)



# --- Main parsing workflow ---
if file:
    st.info("Click 'Parse Model' to extract variables and compute connections.")
    if st.button("Parse Model") or "df_merged" in st.session_state:
        path = save_to_temp(file)

        if "df_merged" not in st.session_state:
            timings = {}

            # Step 1: Raw variable parsing
            with st.spinner("Parsing raw variables from .mdl file..."):
                start = time.time()
                df_raw, debug = extract_raw_variables(path)
                timings['raw_parsing'] = time.time() - start
                st.info(f"Raw variable parsing done in {timings['raw_parsing']:.2f}s")

            # Step 2: PySD views parsing
            with st.spinner("Parsing views from PySD..."):
                start = time.time()
                df_views = parse_views_pysd(path, debug)
                timings['views_parsing'] = time.time() - start
                st.info(f"Views parsing done in {timings['views_parsing']:.2f}s")

            # Step 3: Merge
            with st.spinner("Merging raw variables with views..."):
                start = time.time()
                df_merged = pd.merge(df_raw, df_views, on="Variable", how="left")
                df_merged["View"] = df_merged["View"].fillna("NAN")
                timings['merge'] = time.time() - start
                st.info(f"Merging done in {timings['merge']:.2f}s")

            # Step 4: Build dictionaries
            with st.spinner("Building dictionaries..."):
                start = time.time()
                view_vars: Dict[str, List[str]] = {}
                var_formula: Dict[str, str] = {}
                for _, row in df_merged.iterrows():
                    var_formula[row["Variable"]] = row["Formula"] or ""
                    view_vars.setdefault(row["View"] or "NAN", []).append(row["Variable"])
                timings['dict_build'] = time.time() - start
                st.info(f"Building dictionaries done in {timings['dict_build']:.2f}s")

            # Step 5: Connections
            with st.spinner("Computing view-to-view connections..."):
                start = time.time()
                connections = compute_view_connections(view_vars, var_formula)
                timings['connections'] = time.time() - start
                st.info(f"Connection computation done in {timings['connections']:.2f}s")

            # Step 6: Matrix
            with st.spinner("Generating view-to-view matrix..."):
                start = time.time()
                view_matrix = generate_view_matrix(view_vars, var_formula)
                timings['matrix'] = time.time() - start
                st.info(f"Matrix generation done in {timings['matrix']:.2f}s")

            # Total
            total_elapsed = sum(timings.values())
            st.success(f"All processing completed in {total_elapsed:.2f}s")

            # Save session state
            st.session_state.df_merged = df_merged
            st.session_state.debug = debug
            st.session_state.view_vars = view_vars
            st.session_state.var_formula = var_formula
            st.session_state.connections = connections
            st.session_state.view_matrix = view_matrix
            st.session_state.timings = timings

        # --- Display tables and network ---
        df_merged = st.session_state.df_merged
        st.subheader("Inspect Variables by View")
        st.dataframe(df_merged[["Variable","View","Formula"]], height=200)

        st.subheader("Interactive View Connection Network")
        plot_network(st.session_state.connections)

        csv_matrix = st.session_state.view_matrix.to_csv(index=True)
        st.download_button("Download View-to-View Matrix", csv_matrix, file_name="view_to_view_matrix.csv", mime="text/csv")

        st.subheader("Shared Variables Between Two Views")

        def swap_views():
            st.session_state.view_a, st.session_state.view_b = st.session_state.view_b, st.session_state.view_a

        views_list = sorted(st.session_state.view_vars.keys())
        if views_list:
            col1, col2, col3 = st.columns([2,2,0.5])
            with col1:
                view_a = st.selectbox("View A", views_list, index=0, key="view_a")
            with col2:
                view_b = st.selectbox("View B", views_list, index=min(1,len(views_list)-1), key="view_b")
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("🔄", on_click=swap_views, help="Swap views")

            if st.session_state.view_a != st.session_state.view_b:
                view_a = st.session_state.view_a
                view_b = st.session_state.view_b

                shared = st.session_state.connections.get((view_a, view_b), set())
                if shared:
                    rows = []
                    for var_a in sorted(shared):
                        for var_b in st.session_state.view_vars[view_b]:
                            formula = st.session_state.var_formula.get(var_b, "")
                            if re.search(r'\b' + re.escape(var_a) + r'\b', formula):
                                rows.append({
                                    f"Variable Output from <{view_a}>": var_a,
                                    f"Variable Input into <{view_b}>": var_b,
                                    f"Formula in <{view_b}>": formula
                                })
                    df_shared = pd.DataFrame(rows)
                    st.dataframe(df_shared)
                    csv_shared = df_shared.to_csv(index=False)
                    st.download_button(f"Download Shared Variables ({view_a}_to_{view_b})", csv_shared,
                                       file_name=f"shared_vars_{view_a}_to_{view_b}.csv", mime="text/csv")
                else:
                    st.info("No shared variables found.")

        with st.expander("Diagnostics & Timings"):
            for line in st.session_state.debug:
                st.write(line)
            st.write("Processing timings (s):", st.session_state.timings)
