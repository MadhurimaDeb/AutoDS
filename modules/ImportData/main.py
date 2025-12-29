import streamlit as st
from .ui import render_upload_ui, render_save_button, render_next_step_button
from .helpers import load_data, save_to_cloud

def render_data_import_page():
    st.title("📂 Import & Save Data")

    # 1. Upload UI
    uploaded_file = render_upload_ui()
    df = load_data(uploaded_file)

    # 2. Dataset preview
    if df is not None:
        st.success(f"Successfully loaded '{uploaded_file.name}'")
        
        # AUTO-SAVE (New Request)
        # Automatically save to cloud if not already present
        if "cloud_datasets" not in st.session_state or uploaded_file.name not in st.session_state["cloud_datasets"]:
             msg = save_to_cloud(df, uploaded_file.name)
             st.toast(f"Auto-saved: {msg}", icon="💾")

        # DATA SUMMARY DASHBOARD
        from .data_summary import render_data_summary
        render_data_summary(df)

        # ⭐ NEW — next step button
        if render_next_step_button():
            # Already auto-saved above
            st.session_state.page = "cleaning"
            st.rerun()

        st.divider()
        with st.expander("🤖 Ask AI about this dataset"):
            if st.button("Analyze Schema"):
                prompt = "Analyze these columns and suggest what this data might be useful for."
                summary = f"Columns: {list(df.columns)}\nDtypes:\n{df.dtypes}"
                insight = st.session_state.chat_manager.generate_insight(prompt, summary)
                st.write(insight)


    # 4. Show cloud datasets
    if "cloud_datasets" in st.session_state:
        st.write("### 📁 Datasets in Cloud Memory:")
        from core.data_manager import DataManager
        
        # Using a container for better layout
        stored_datasets = list(st.session_state["cloud_datasets"].keys())
        if not stored_datasets:
            st.info("No datasets currently in memory.")
        
        for name in stored_datasets:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.info(f"📄 {name}")
            with col2:
                if st.button("🗑️", key=f"del_{name}", help=f"Delete {name}"):
                    # 1. Delete from disk
                    if DataManager.delete_dataset(name):
                        st.toast(f"Deleted {name} from disk.", icon="🗑️")
                    else:
                        st.warning(f"Could not delete {name} from disk (maybe it doesn't exist).")
                    
                    # 2. Delete from session
                    del st.session_state["cloud_datasets"][name]
                    
                    # 3. If it was active, clear active
                    if st.session_state.get("active_dataset") == name:
                        st.session_state["active_dataset"] = None
                        st.session_state["active_dataset_path"] = None
                    
                    st.rerun()
