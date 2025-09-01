import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="🔁",
)

st.write("# Suite of Vensim Internal Tools")

st.sidebar.success("Select Tools Above")

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

st.markdown(
    """
    This suite of tools is designed for large Vensim-based System Dynamics (SD) projects
    that are often contained in single files. These tools are meant to compensate for the inflexibilities of compartmentalization that arise from the strong visual elements of system dynamics models, as compared to traditional code-based models. By using these tools, you can enhance internal understanding 
    of existing model versions as part of your workflow.

    #### 👈 Key Tools
    1. **⚖️ Version Comparison**  
       Compare two versions of a model not just visually, but also at the level of their **mathematical formulation**. 
       This ensures consistency and reveals meaningful changes beyond the visual diagrams.

    2. **🧩 Sub Model Analysis**  
       When a model has multiple views representing different modules, this tool helps you understand 
       how modules are linked through shadow variables. It exposes the **linkages** embedded in the SD model, 
       making it easier to understand the conceptual structure of the model.
    """
)
