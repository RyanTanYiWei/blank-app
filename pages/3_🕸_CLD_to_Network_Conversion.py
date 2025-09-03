import streamlit as st
from pathlib import Path
import tempfile
import pandas as pd
import re
import networkx as nx

# --- Page config ---
st.set_page_config(layout="wide", page_title="CLD_to_Network_Conversion", page_icon="🕸")

# --- Load external CSS ---
css_file = Path(__file__).parent.parent / "assets" / "style.css"
if css_file.exists():
    css_content = css_file.read_text()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


st.title("🕸 CLD to Network Conversion")
st.caption("Oh, You Do System Dynamics and Network Analysis?")
st.warning("⚠️ This tool assumes a single view in the Vensim Model.")

st.markdown("""
Upload a `.mdl` file. This tool will:  
🔹 **Extract** nodes & edges  
🔹 **Display** interactive network graph  
🔹 **Detect** feedback loops to highlight  
🔹 **Download** node & edge as CSVs  
""")

# --- File upload ---
file = st.file_uploader("Vensim model (.mdl)", type=["mdl"])

def save_to_temp(uploaded_file) -> Path:
    if not uploaded_file:
        return None
    tmp_dir = Path(tempfile.mkdtemp(prefix="mdl_"))
    tmp_path = tmp_dir / Path(uploaded_file.name).name
    tmp_path.write_bytes(uploaded_file.read())
    return tmp_path

def parse_mdl_sketch(model_path: Path):
    text = Path(model_path).read_text(errors="ignore")
    sketch_pattern = re.compile(r"\\{3}---/// Sketch information.*?///---\\\\", re.DOTALL)
    sketch_match = sketch_pattern.search(text)
    if not sketch_match:
        raise ValueError("No Sketch block found in mdl file")
    sketch_text = sketch_match.group(0)

    nodes, edges = {}, []
    for line in sketch_text.splitlines():
        parts = line.strip().split(",")
        if parts[0] == "10":
            nodes[parts[1]] = parts[2]
    for line in sketch_text.splitlines():
        parts = line.strip().split(",")
        if parts[0] == "1":
            src = nodes.get(parts[2], f"ID_{parts[2]}")
            tgt = nodes.get(parts[3], f"ID_{parts[3]}")
            pol_code = int(parts[6]) if len(parts) > 6 and parts[6].isdigit() else 0
            dtype_val = int(parts[9]) if len(parts) > 9 and parts[9].isdigit() else 0
            polarity = "+" if pol_code==43 else "-" if pol_code==45 else "neutral"
            delay = dtype_val==193
            edges.append({"Source": src,"Target": tgt,"Polarity": polarity,"Delay": delay})
    return sorted(nodes.values()), edges

def find_loops(edges):
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e["Source"], e["Target"])
    return list(nx.simple_cycles(G))

def plot_network(nodes, edges, highlight_nodes=None, highlight_edges=None, saved_positions=None):
    try:
        from pyvis.network import Network
        import streamlit.components.v1 as components
        import tempfile
        from pathlib import Path
    except Exception as e:
        st.warning(f"Visualization libraries not available: {e}")
        return

    net = Network(height="500px", width="100%", directed=True,
                  bgcolor="#ffffff", font_color="black", notebook=False)

    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e["Source"], e["Target"])
    node_degree = {node: 0 for node in nodes}
    for e in edges:
        node_degree[e["Source"]] += 1
        node_degree[e["Target"]] += 1
    max_degree = max(node_degree.values()) if node_degree else 1
    min_degree = min(node_degree.values()) if node_degree else 0

    # Compute positions
    pos = saved_positions if saved_positions else nx.kamada_kawai_layout(G)
    positions_out = pos

    # Add nodes
    for node in nodes:
        size = 12 + (node_degree.get(node,0) - min_degree)/max(1,max_degree-min_degree)*30
        color = "#97c2fc"
        border_color = "#ff00ff" if highlight_nodes and node in highlight_nodes else "#000000"
        border_width = 4 if highlight_nodes and node in highlight_nodes else 1
        x, y = pos[node]
        net.add_node(node, label=node, size=size,
                     color={"border": border_color, "background": color},
                     borderWidth=border_width, x=x*500, y=y*500)

    # Add edges
    for edge in edges:
        src, tgt = edge["Source"], edge["Target"]
        pol = edge["Polarity"]
        delay = edge["Delay"]
        default_color = {"+" : "green", "-" : "red", "neutral":"#848484"}[pol]
        color = "#ff00ff" if highlight_edges and (src,tgt) in highlight_edges else default_color
        label = "=" if delay else ""
        width = 3 if highlight_edges and (src,tgt) in highlight_edges else 2
        net.add_edge(src, tgt, color=color, width=width, label=label, title=pol)

    net.toggle_physics(False)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.save_graph(tmp_file.name)
    components.html(Path(tmp_file.name).read_text(), height=500)
    return positions_out

# --- Main workflow ---
if file:
    path = save_to_temp(file)
    try:
        nodes, edges = parse_mdl_sketch(path)

        st.subheader("Node and Edge Lists")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Nodes**")
            node_df = pd.DataFrame(nodes, columns=["Variable"])
            st.dataframe(node_df, height=250, use_container_width=True)
        with col2:
            st.markdown("**Edges (Polarity & Delay)**")
            edge_df = pd.DataFrame(edges)
            st.dataframe(edge_df, height=250, use_container_width=True)

        # Downloads
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Download Node List (CSV)", node_df.to_csv(index=False),
                               file_name="nodes.csv", mime="text/csv")
        with col2:
            st.download_button("⬇️ Download Edge List (CSV)", edge_df.to_csv(index=False),
                               file_name="edges.csv", mime="text/csv")

        loops = find_loops(edges)
        highlighted_nodes = set()
        highlighted_edges = set()

        # Side-by-side: loops + network
        col1, col2 = st.columns([2,3])
        with col1:
            st.subheader("Feedback Loops")
            if loops:
                loop_names = ["No Highlight"] + [f"Loop {i+1}: {' → '.join(loop)}" for i, loop in enumerate(loops)]
                selected_loop = st.radio("Select a loop to highlight", loop_names, index=0)

                if selected_loop != "No Highlight":
                    idx = loop_names.index(selected_loop) - 1  # adjust for No Highlight at index 0
                    highlighted_nodes = set(loops[idx])
                    loop_edges = set()
                    for i in range(len(loops[idx])):
                        s, t = loops[idx][i], loops[idx][(i+1)%len(loops[idx])]
                        loop_edges.add((s,t))
                    highlighted_edges = loop_edges
            else:
                st.info("No loops detected.")

        with col2:
            st.subheader("Network Graph")
            if "node_positions" not in st.session_state:
                st.session_state.node_positions = None
            positions = plot_network(
                nodes, edges,
                highlight_nodes=highlighted_nodes,
                highlight_edges=highlighted_edges,
                saved_positions=st.session_state.node_positions
            )
            st.session_state.node_positions = positions

    except Exception as e:
        st.error(f"Parsing failed: {e}")
