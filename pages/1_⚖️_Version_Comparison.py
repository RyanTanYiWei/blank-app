import streamlit as st
import tempfile
from pathlib import Path
from typing import Dict, Tuple, List

st.set_page_config(layout="wide", page_title="Version Comparisons", page_icon="⚖️")
st.markdown(
    """
    <style>
      .block-container {max-width: 1800px; padding-left: 10rem; padding-right: 10rem;}
      /* Wrap long code blocks without changing colors */
      pre, code { white-space: pre-wrap; overflow-wrap: anywhere; word-break: break-word; }
      /* Add subtle separation around code blocks */
      pre { border: 1px solid rgba(0,0,0,0.08); border-radius: 6px; padding: 0.75rem; }

      /* Make metrics cards more card-like */
      [data-testid="stMetricValue"] {
          font-size: 1.5rem;
          font-weight: 700;
          color: #2e86de;
      }
      [data-testid="stMetricLabel"] {
          font-size: 0.9rem;
          font-weight: 500;
          opacity: 0.8;
      }

      /* Space and shadow for metric blocks */
      .css-1ht1j8u, .css-1r6slb0 {
          padding: 1rem !important;
          border-radius: 12px !important;
          box-shadow: 0 2px 6px rgba(0,0,0,0.08);
          background: #ffffff;
      }

      /* Section headers */
      h2, h3, .stSubheader {
          color: #1a5276;
          border-bottom: 1px solid rgba(0,0,0,0.1);
          padding-bottom: 0.3rem;
          margin-bottom: 1rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚖️ Version Comparisons")
st.caption("Built for Modelling Teams with Terrible Version Control Practices")
st.warning(
    "⚠️ This tool assumes two model files represent different **versions** of the same model."
)
st.markdown(
    """
    Upload two `.mdl` files to compare. The tool will show:  
    🔹 **Changed formulas** for variables present in both models  
    🔹 **New variables in Model A**  
    🔹 **New variables in Model B**

    """
    )

col1, col2 = st.columns(2)
with col1:
    file_a = st.file_uploader("First Vensim model (.mdl)", type=["mdl"], key="file_a")
with col2:
    file_b = st.file_uploader("Second Vensim model (.mdl)", type=["mdl"], key="file_b")


def save_to_temp(uploaded_file) -> Path:
    if not uploaded_file:
        return None
    tmp_dir = Path(tempfile.mkdtemp(prefix="vensim_"))
    tmp_path = tmp_dir / Path(uploaded_file.name).name
    tmp_path.write_bytes(uploaded_file.read())
    return tmp_path


def extract_equations_with_pysd(model_path: Path) -> Tuple[Dict[str, str], List[str]]:
    try:
        import pysd
    except Exception as e:
        return {}, [f"PySD import failed: {e}"]

    equations: Dict[str, str] = {}
    debug: List[str] = [f"Using PySD {getattr(pysd, '__version__', 'unknown')} for '{model_path.name}'"]

    # First, try raw Vensim parse (works even if model can't run)
    try:
        from pysd.translators.vensim.vensim_file import VensimFile  # type: ignore
        vf = VensimFile(str(model_path))
        vf.parse()
        sections = getattr(vf, "sections", []) or []
        debug.append(f"Raw parse sections: {len(sections)}")

        def _stringify_equation(obj):
            for attr in [
                "rhs", "equation", "expr", "expression", "raw_equation", "raw", "text", "value", "definition",
            ]:
                val = getattr(obj, attr, None)
                if val is not None:
                    return str(val)
            for method in ["to_vensim", "to_text", "to_string"]:
                fn = getattr(obj, method, None)
                if callable(fn):
                    try:
                        return str(fn())
                    except Exception:
                        pass
            try:
                return repr(obj)
            except Exception:
                return None

        for section in sections:
            elements = getattr(section, "elements", []) or []
            debug.append(f"Section elements: {len(elements)}")
            for element in elements:
                name = (
                    getattr(element, "name", None)
                    or getattr(element, "canon_name", None)
                    or getattr(getattr(element, "component", None) or object(), "name", None)
                )
                equation_text = _stringify_equation(element)
                component = getattr(element, "component", None)
                if (not equation_text or len(equation_text) < 2) and component is not None:
                    eq2 = _stringify_equation(component)
                    if eq2 and len(eq2) > 1:
                        equation_text = eq2
                if name and equation_text:
                    equations[str(name)] = str(equation_text).strip()
        debug.append(f"Raw parse equations extracted: {len(equations)}")
    except Exception as e:
        debug.append(f"Raw parse failed: {e}")

    # If raw parse failed to produce results, try translation-based model
    if not equations:
        try:
            model = pysd.read_vensim(str(model_path))
            debug.append("Translation succeeded")
        except Exception as e:
            debug.append(f"Translation failed: {e}")
            return {}, debug

        doc = getattr(model, "doc", None)
        if doc is not None:
            try:
                name_col = "Real Name" if "Real Name" in doc.columns else None
                eq_col = "Equation" if "Equation" in doc.columns else None
                debug.append(f"model.doc rows: {len(doc)}; cols: {list(doc.columns)}")
                alt_eq_cols = [c for c in ["Eqn", "Formula", "Definition"] if c in getattr(doc, "columns", [])]
                if name_col and (eq_col or alt_eq_cols):
                    for _, row in doc.iterrows():
                        name = str(row[name_col]).strip()
                        eq_val = row[eq_col] if eq_col else row[alt_eq_cols[0]]
                        eq = str(eq_val).strip()
                        if name:
                            equations[name] = eq
            except Exception as e:
                debug.append(f"Reading model.doc failed: {e}")

        if not equations:
            try:
                possible_containers = [
                    getattr(model, "components", None),
                    getattr(model, "_namespace", None),
                    getattr(getattr(model, "components", None) or object(), "_namespace", None),
                    getattr(getattr(model, "components", None) or object(), "namespace", None),
                    getattr(getattr(model, "components", None) or object(), "elements", None),
                ]
                found_any = False
                for container in possible_containers:
                    if not container:
                        continue
                    if hasattr(container, "items"):
                        found_any = True
                        debug.append(f"Namespace container items: {len(list(container.items()))}")
                        for name, meta in container.items():
                            eq = None
                            if isinstance(meta, dict):
                                eq = meta.get("orig_eqn") or meta.get("equation") or meta.get("eqn")
                            if eq is None and hasattr(meta, "get"):
                                try:
                                    eq = meta.get("equation")
                                except Exception:
                                    pass
                            if eq:
                                equations[str(name)] = str(eq).strip()
                    else:
                        for attr in ["_namespace", "namespace", "elements"]:
                            ns = getattr(container, attr, None)
                            if hasattr(ns, "items"):
                                found_any = True
                                debug.append(f"Namespace via {attr}: {len(list(ns.items()))}")
                                for name, meta in ns.items():
                                    eq = None
                                    if isinstance(meta, dict):
                                        eq = meta.get("orig_eqn") or meta.get("equation") or meta.get("eqn")
                                    if eq:
                                        equations[str(name)] = str(eq).strip()
                if not found_any:
                    raise AttributeError("No namespace container found on model")
            except Exception as e:
                debug.append(f"Reading components namespace failed: {e}")

    return equations, debug


def diff_equation_maps(a: Dict[str, str], b: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, Tuple[str, str]], Dict[str, str]]:
    only_in_a = {k: a[k] for k in a.keys() - b.keys()}
    only_in_b = {k: b[k] for k in b.keys() - a.keys()}
    changed = {}
    for k in a.keys() & b.keys():
        if (a.get(k) or "").strip() != (b.get(k) or "").strip():
            changed[k] = (a.get(k, ""), b.get(k, ""))
    return only_in_a, changed, only_in_b


if file_a and file_b:
    recompute = st.button("Compare Models")
    st.info("Click 'Compare Model' to extract equations and compare changes.")
    if recompute:
        with st.spinner("Parsing models with PySD..."):
            path_a = save_to_temp(file_a)
            path_b = save_to_temp(file_b)
            eq_a, dbg_a = extract_equations_with_pysd(path_a)
            eq_b, dbg_b = extract_equations_with_pysd(path_b)
        st.session_state["_diff_result"] = {
            "eq_a": eq_a,
            "eq_b": eq_b,
            "dbg_a": dbg_a,
            "dbg_b": dbg_b,
            "a_name": Path(file_a.name).name,
            "b_name": Path(file_b.name).name,
        }

    diff = st.session_state.get("_diff_result")
    if diff:
        eq_a = diff["eq_a"]; eq_b = diff["eq_b"]
        dbg_a = diff["dbg_a"]; dbg_b = diff["dbg_b"]
        a_name = diff["a_name"]; b_name = diff["b_name"]

        if not eq_a or not eq_b:
            st.warning("Unable to extract equations from one or both models.")
            with st.expander("Diagnostics: Model A"):
                for line in dbg_a:
                    st.write(line)
                st.write(f"Equations extracted: {len(eq_a)}")
            with st.expander("Diagnostics: Model B"):
                for line in dbg_b:
                    st.write(line)
                st.write(f"Equations extracted: {len(eq_b)}")
        else:
            only_a, changed, only_b = diff_equation_maps(eq_a, eq_b)

            total_a = len(eq_a)
            total_b = len(eq_b)
            common = set(eq_a.keys()) & set(eq_b.keys())
            changed_count = len(changed)
            similar_count = max(len(common) - changed_count, 0)

            # --- Unified Summary ---
            st.subheader("Summary")
            c1, c2, c3 = st.columns(3)
            c4, c5, c6 = st.columns(3)

            c1.metric(label=f"Variables in {a_name}", value=total_a)
            c2.metric(label=f"Variables in {b_name}", value=total_b)
            c3.metric(label="Common", value=len(common))
            c4.metric(label="Similar", value=similar_count)
            c5.metric(label="Changed", value=changed_count)
            c6.metric(label=f"Only in {a_name}/{b_name}", value=f"{len(only_a)} / {len(only_b)}")

            # --- Render differences ---
            def _render_truncated(label: str, text: str, max_chars: int = 200):
                if text is None:
                    text = ""
                text = str(text)
                truncated = text if len(text) <= max_chars else text[:max_chars] + " …"
                st.code(text) # no truncation

            def render_changed():
                if not changed:
                    st.info("No changed formulas.")
                    return
                with st.expander("Changed formulas (expand/collapse)", expanded=True):
                    for name, (ea, eb) in sorted(changed.items()):
                        st.markdown(f"<div style='font-weight:600; font-size:0.95rem; margin-bottom:0.5rem;'>{name}</div>", unsafe_allow_html=True)
                        col_left, col_right = st.columns(2)

                        with col_left:
                            st.markdown(f"<div style='font-weight:500; opacity:0.7; margin-bottom:0.25rem;'>{a_name} formula:</div>", unsafe_allow_html=True)
                            _render_truncated("", ea, max_chars=400)

                        with col_right:
                            st.markdown(f"<div style='font-weight:500; opacity:0.7; margin-bottom:0.25rem;'>{b_name} formula:</div>", unsafe_allow_html=True)
                            _render_truncated("", eb, max_chars=400)

                        st.markdown("<hr style='border:none; border-top:1px solid rgba(0,0,0,0.08); margin:0.5rem 0;'>", unsafe_allow_html=True)


            def render_only_a():
                if not only_a:
                    st.info(f"No variables only in {a_name}.")
                    return
                with st.expander(f"Only in {a_name} (expand/collapse)", expanded=True):
                    for name, eq in sorted(only_a.items()):
                        st.markdown(f"- **{name}**")
                        _render_truncated(f"{a_name} formula", eq)

            def render_only_b():
                if not only_b:
                    st.info(f"No variables only in {b_name}.")
                    return
                with st.expander(f"Only in {b_name} (expand/collapse)", expanded=True):
                    for name, eq in sorted(only_b.items()):
                        st.markdown(f"- **{name}**")
                        _render_truncated(f"{b_name} formula", eq)

            render_changed()
            render_only_a()
            render_only_b()

            # CSV export
            import io, csv
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Type", "Name", a_name + " Equation", b_name + " Equation"])
            for name, (ea, eb) in changed.items():
                writer.writerow(["changed", name, ea, eb])
            for name, ea in only_a.items():
                writer.writerow(["only_in_a", name, ea, ""]) 
            for name, eb in only_b.items():
                writer.writerow(["only_in_b", name, "", eb])
            st.download_button(
                label="Download differences (CSV)",
                data=output.getvalue(),
                file_name=f"vensim_formula_diff_{a_name}_vs_{b_name}.csv",
                mime="text/csv",
            )
