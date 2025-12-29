import os
import pandas as pd
import streamlit as st
import datetime
import glob

DATA_DIR = os.path.join(os.getcwd(), "data")

class DataManager:
    @staticmethod
    def _ensure_data_dir():
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def save_dataset(df: pd.DataFrame, filename: str, version_note: str = "initial", action_description: str = None):
        """
        Save dataframe as parquet and log the action.
        """
        DataManager._ensure_data_dir()
        
        # Clean filename
        clean_name = filename.split(".")[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        save_name = f"{clean_name}_v{timestamp}_{version_note}.parquet"
        file_path = os.path.join(DATA_DIR, save_name)
        
        df.to_parquet(file_path, index=False)
        
        # Update session state to reflect this as active
        st.session_state["active_dataset_path"] = file_path
        st.session_state["active_dataset"] = os.path.basename(file_path)
        
        # Log Action
        if action_description:
            if "action_log" not in st.session_state: st.session_state["action_log"] = []
            
            # Add timestamp to log
            # Format: [14:05:00] Dropped 3 columns
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{time_str}] {action_description}"
            st.session_state["action_log"].append(log_entry)
        
        return file_path

    @staticmethod
    def list_datasets():
        """List all available parquet datasets in data dir."""
        DataManager._ensure_data_dir()
        files = glob.glob(os.path.join(DATA_DIR, "*.parquet"))
        dataset_options = []
        for f in sorted(files, reverse=True):
            dataset_options.append(os.path.basename(f))
        return dataset_options

    @staticmethod
    def load_dataset(file_name: str):
        """Load a specific dataset file."""
        file_path = os.path.join(DATA_DIR, file_name)
        if os.path.exists(file_path):
            return pd.read_parquet(file_path)
        return None

    @staticmethod
    def get_latest_version(dataset_id: str):
        """Get the most recent version of a dataset."""
        DataManager._ensure_data_dir()
        files = glob.glob(os.path.join(DATA_DIR, f"{dataset_id}_v*.parquet"))
        if not files:
            return None
        # Sort by name (which includes timestamp) to get latest
        return pd.read_parquet(sorted(files)[-1])

    @staticmethod
    def delete_dataset(filename: str) -> bool:
        """Delete a dataset file from disk."""
        DataManager._ensure_data_dir()
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        return False
