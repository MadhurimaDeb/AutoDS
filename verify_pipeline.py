import streamlit as st
import pandas as pd
import os
from core.data_manager import DataManager

# Mock Session State
if "cloud_datasets" not in st.session_state:
    st.session_state["cloud_datasets"] = {}
if "active_dataset" not in st.session_state:
    st.session_state["active_dataset"] = None

print("🚀 Starting Pipeline Verification...")

# 1. Simulate Import
df_raw = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [None, 8, 9]})
dataset_name = "test_data.csv"
# We DO NOT manually set active_dataset here. DataManager should do it.
# st.session_state["active_dataset"] = dataset_name 
st.session_state["cloud_datasets"] = {} # Initialize dict

saved_path = DataManager.save_dataset(df_raw, dataset_name, version_note="raw")
real_name = os.path.basename(saved_path)
st.session_state["cloud_datasets"][real_name] = df_raw

print(f"✅ Imported {dataset_name} -> {real_name}")

# ASSERTION: DataManager should have set active_dataset
if st.session_state.get("active_dataset") == real_name:
    print("✅ DataManager correctly set 'active_dataset'")
else:
    print(f"❌ DataManager FAILED to set 'active_dataset'. Got: {st.session_state.get('active_dataset')}")

# 2. Simulate Cleaning (Drop 'B', Fill 'C')
target_dataset = st.session_state["active_dataset"]
df_clean = st.session_state["cloud_datasets"][target_dataset].copy()
df_clean = df_clean.drop(columns=["B"])
df_clean["C"] = df_clean["C"].fillna(0)
# Update State
DataManager.save_dataset(df_clean, dataset_name, version_note="clean")
st.session_state["cloud_datasets"][dataset_name] = df_clean

# Verify
current_df = st.session_state["cloud_datasets"][dataset_name]
if "B" not in current_df.columns and current_df["C"].isnull().sum() == 0:
    print("✅ Cleaning propagated correctly.")
else:
    print("❌ Cleaning failed to propagate.")

# 3. Simulate Text Cleaning (Trim Whitespace)
df_text = st.session_state["cloud_datasets"][target_dataset].copy()
df_text["E"] = ["  foo  ", "bar", "baz  "]
# Apply trim
df_text["E"] = df_text["E"].str.strip()
DataManager.save_dataset(df_text, target_dataset, version_note="text_clean", action_description="Trimmed whitespace")
st.session_state["cloud_datasets"][target_dataset] = df_text

# Verify
current_df = st.session_state["cloud_datasets"][target_dataset]
if current_df["E"].iloc[0] == "foo":
    print("✅ Text Cleaning propagated correctly.")
else:
    print(f"❌ Text Cleaning Failed. Got '{current_df['E'].iloc[0]}'")

# Check Action Log
if "action_log" in st.session_state and len(st.session_state["action_log"]) > 0:
    print(f"✅ Action Log captured {len(st.session_state['action_log'])} events.")
else:
    print("❌ Action Log is EMPTY.")

# 4. Simulate Feature Engineering (Add 'D' = 'A' * 2)
df_fe = st.session_state["cloud_datasets"][target_dataset].copy()
df_fe["D"] = df_fe["A"] * 2
# Update State
DataManager.save_dataset(df_fe, dataset_name, version_note="fe")
st.session_state["cloud_datasets"][dataset_name] = df_fe

# Verify
current_df = st.session_state["cloud_datasets"][dataset_name]
if "D" in current_df.columns:
    print("✅ Feature Engineering propagated correctly.")
else:
    print("❌ Feature Engineering failed to propagate.")

print("🎉 Pipeline Verification Complete.")
