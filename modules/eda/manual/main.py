import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# PLOT CONFIGURATION
# Defines the rules for each plot type: what data it needs.
# ---------------------------------------------------------
PLOT_CONFIG = {
    "Scatter (2D)": {
        "description": "Analyze relationship between two numerical variables.",
        "func": px.scatter,
        "params": [
            {"arg": "x", "label": "X Axis", "type": "numeric", "req": True},
            {"arg": "y", "label": "Y Axis", "type": "numeric", "req": True},
            {"arg": "color", "label": "Color (Hue)", "type": "all", "req": False},
            {"arg": "size", "label": "Size (Bubble)", "type": "numeric", "req": False},
            {"arg": "hover_name", "label": "Hover Details", "type": "all", "req": False}
        ]
    },
    "Scatter (3D)": {
        "description": "Analyze relationship between three numerical variables in 3D space.",
        "func": px.scatter_3d,
        "params": [
            {"arg": "x", "label": "X Axis", "type": "numeric", "req": True},
            {"arg": "y", "label": "Y Axis", "type": "numeric", "req": True},
            {"arg": "z", "label": "Z Axis", "type": "numeric", "req": True},
            {"arg": "color", "label": "Color (Group)", "type": "all", "req": False},
            {"arg": "size", "label": "Size", "type": "numeric", "req": False}
        ]
    },
    "Line Chart": {
        "description": "View trends over a sequence (usually time or index).",
        "func": px.line,
        "params": [
            {"arg": "x", "label": "X Axis (Time/seq)", "type": "all", "req": True},
            {"arg": "y", "label": "Y Axis (Value)", "type": "numeric", "req": True},
            {"arg": "color", "label": "Lines (Group)", "type": "all", "req": False}
        ]
    },
    "Bar Chart": {
        "description": "Compare categories using numeric values.",
        "func": px.bar,
        "params": [
            {"arg": "x", "label": "Category (X)", "type": "all", "req": True},
            {"arg": "y", "label": "Value (Y)", "type": "numeric", "req": True},
            {"arg": "color", "label": "Stack/Group", "type": "all", "req": False},
            {"arg": "barmode", "label": "Mode", "type": "select", "options": ["group", "stack", "relative"], "req": True, "default": "group"}
        ]
    },
    "Histogram (Distribution)": {
        "description": "View the frequency distribution of a variable.",
        "func": px.histogram,
        "params": [
            {"arg": "x", "label": "Variable", "type": "numeric", "req": True},
            {"arg": "color", "label": "Split by", "type": "all", "req": False},
            {"arg": "nbins", "label": "Bins", "type": "slider", "min": 5, "max": 100, "default": 30, "req": True}
        ]
    },
    "Box Plot": {
        "description": "Analyze statistical distribution and outliers.",
        "func": px.box,
        "params": [
            {"arg": "x", "label": "Category (X)", "type": "all", "req": False},
            {"arg": "y", "label": "Value (Y)", "type": "numeric", "req": True},
            {"arg": "color", "label": "Split by", "type": "all", "req": False}
        ]
    },
    "Parallel Coordinates": {
        "description": "Compare many numeric variables side-by-side (High Dimensional).",
        "func": px.parallel_coordinates,
        "params": [
            {"arg": "dimensions", "label": "Select Variables (Multi)", "type": "multiselect_numeric", "req": True},
            {"arg": "color", "label": "Color Scale Variable", "type": "numeric", "req": True}
        ]
    },
    "Scatter Matrix (Pair Plot)": {
        "description": "View all pairwise relationships in a grid.",
        "func": px.scatter_matrix,
        "params": [
            {"arg": "dimensions", "label": "Select Variables (Multi)", "type": "multiselect_numeric", "req": True},
            {"arg": "color", "label": "Color (Group)", "type": "all", "req": False}
        ]
    },
     "Density Heatmap": {
        "description": "2D Distribution density (useful for large data).",
        "func": px.density_heatmap,
        "params": [
            {"arg": "x", "label": "X Axis", "type": "numeric", "req": True},
            {"arg": "y", "label": "Y Axis", "type": "numeric", "req": True},
             {"arg": "z", "label": "Z (Agg)", "type": "numeric", "req": False}
        ]
    },
}

def render_manual_eda():
    st.header("🎨 Smart Manual EDA")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    dataset_name = st.session_state["active_dataset"]
    df = st.session_state["cloud_datasets"][dataset_name]
    
    # Identify Column Types
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    all_cols = df.columns.tolist()

    # 1. Plot Selection
    st.caption(f"Analyzing: **{dataset_name}** ({df.shape[0]} rows, {df.shape[1]} cols)")
    
    plot_names = list(PLOT_CONFIG.keys())
    selected_plot_name = st.selectbox("1️⃣ Select Plot Type", plot_names)
    
    config = PLOT_CONFIG[selected_plot_name]
    st.info(f"ℹ️ {config['description']}")
    
    # 2. Dynamic Configuration
    st.write("2️⃣ Configure Axes")
    plot_args = {}
    
    # Use 3 columns for controls
    cols = st.columns(3)
    col_idx = 0
    
    valid_config = True
    
    for param in config["params"]:
        key = param["arg"]
        label = param["label"]
        p_type = param["type"]
        is_req = param.get("req", False)
        
        # Determine eligible columns
        options = []
        if p_type == "numeric": options = num_cols
        elif p_type == "categorical": options = cat_cols
        elif p_type == "all": options = all_cols
        
        # Layout
        with cols[col_idx % 3]:
            # Handle different input widget types
            if p_type == "slider":
                val = st.slider(label, param["min"], param["max"], param["default"])
                plot_args[key] = val
                
            elif p_type == "select":
                val = st.selectbox(label, param["options"], index=0)
                plot_args[key] = val
                
            elif p_type == "multiselect_numeric":
                val = st.multiselect(label, num_cols, default=num_cols[:4] if len(num_cols) > 4 else num_cols)
                if not val and is_req: valid_config = False
                plot_args[key] = val
                
            else: # Standard Column Selector
                # Add "None" option if optional
                final_opts = ["None"] + options if not is_req else options
                
                # Default index logic (try to be smart)
                idx = 0
                # If X/Y, try to pick different defaults
                if key == "x" and len(options) > 0: idx = 0
                if key == "y" and len(options) > 1: idx = 1
                if key == "z" and len(options) > 2: idx = 2
                
                # Render
                selection = st.selectbox(label, final_opts, index=idx if idx < len(final_opts) else 0, key=f"sel_{key}")
                
                if selection != "None":
                    plot_args[key] = selection
                elif is_req:
                    valid_config = False # Missing required arg
        
        col_idx += 1

    st.divider()

    # 3. Plot & AI
    if st.button("🚀 Generate Plot", type="primary", use_container_width=True):
        if not valid_config:
            st.error("Please select all required fields (X, Y, etc).")
        else:
            try:
                # Generate Plot
                func = config["func"]
                clean_args = {k: v for k, v in plot_args.items() if v is not None}
                
                fig = func(df, **clean_args)
                
                # Store in Session State
                st.session_state["eda_fig"] = fig
                
                # Store Context for AI
                details = [f"{k}: {v}" for k, v in clean_args.items()]
                st.session_state["eda_context"] = f"Plot Type: {selected_plot_name}\nConfiguration:\n" + "\n".join(details)
                
            except Exception as e:
                st.error(f"Plotting Error: {e}")

    # 4. Render from State (Persistent)
    if "eda_fig" in st.session_state:
        st.plotly_chart(st.session_state["eda_fig"], use_container_width=True)
        
        with st.expander("🤖 AI Insights (Context Aware)", expanded=True):
            st.write("Ask the AI to explain this specific plot.")
            if st.button("🧠 Interpret this Result"):
                if "eda_context" in st.session_state:
                    context = f"I have generated a plot for dataset '{dataset_name}'.\n{st.session_state['eda_context']}"
                    prompt = f"{context}\nPlease analyze what kind of patterns, outliers, or clusters we should look for in this chart. If possible, hypothesize about the relationships shown."
                    
                    response = st.session_state.chat_manager.generate_insight(prompt)
                    st.write(response)
                else:
                    st.warning("Please generate a plot first.")
