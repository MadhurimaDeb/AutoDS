import streamlit as st
import pandas as pd
import io

def render_dataset_manager():
    """
    Render a sidebar widget to manage the active dataset (Select, Download).
    """
    st.sidebar.divider()
    st.sidebar.subheader("🗂️ Dataset Manager")
    
    # 1. Check if we have datasets
    if "cloud_datasets" not in st.session_state or not st.session_state["cloud_datasets"]:
        st.sidebar.info("No datasets imported yet.")
        return

    datasets = list(st.session_state["cloud_datasets"].keys())
    
    # 2. Selector
    # Default to current active if valid
    current_active = st.session_state.get("active_dataset")
    if current_active not in datasets:
        current_active = datasets[0] if datasets else None
    
    selected_dataset = st.sidebar.selectbox(
        "Active Dataset",
        datasets,
        index=datasets.index(current_active) if current_active else 0,
        key="global_dataset_selector"
    )
    
    # Update state if changed
    if selected_dataset != st.session_state.get("active_dataset"):
        st.session_state["active_dataset"] = selected_dataset
        # We don't easily know the path unless we stored a mapping, 
        # but active_dataset_path is less critical if we use the dict
        # We can try to infer or just set it to None to avoid stale paths
        st.session_state["active_dataset_path"] = None 
        st.rerun()

    # 3. Export Options
    df = st.session_state["cloud_datasets"][selected_dataset]
    
    col1, col2 = st.sidebar.columns(2)
    
    # CSV Download
    csv = df.to_csv(index=False).encode('utf-8')
    col1.download_button(
        label="📥 CSV",
        data=csv,
        file_name=f"{selected_dataset}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Excel Download
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    col2.download_button(
        label="📥 Excel",
        data=buffer.getvalue(),
        file_name=f"{selected_dataset}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
