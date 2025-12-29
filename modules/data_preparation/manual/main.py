import streamlit as st
import pandas as pd
import numpy as np
from core.data_manager import DataManager
import os

def render_manual_cleaning():
    st.header("🛠️ Comprehensive Data Cleaning")
    
    if "active_dataset" not in st.session_state:
        st.warning("Please import a dataset first.")
        return

    dataset_name = st.session_state["active_dataset"]
    df = st.session_state["cloud_datasets"][dataset_name]
    
    st.write(f"**Target Dataset:** `{dataset_name}` | **Shape:** {df.shape}")
    st.dataframe(df.head())
    
    # ---------------------------------------------------------
    # 0. CONTEXT ANALYSIS
    # ---------------------------------------------------------
    has_missing = df.isnull().values.any()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    text_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    
    # ---------------------------------------------------------
    # 1. ADVANCED COLUMN OPERATIONS (13 Categories)
    # ---------------------------------------------------------
    from .column_ops import COLUMN_OPS_CATALOG, apply_column_operation
    
    with st.expander("🛠️ Advanced Column Operations (Structure, Types, Filter...)", expanded=True):
        
        # 1. Filter Keys based on Context
        available_cats = list(COLUMN_OPS_CATALOG.keys())
        
        # Rule: Hide Missing ops if no missing values
        if not has_missing:
            available_cats = [c for c in available_cats if "Missing" not in c]
            
        # Category Selector
        c_cat, c_meth = st.columns(2)
        cat = c_cat.selectbox("Operation Category", available_cats)
        
        if cat:
            meth_options = COLUMN_OPS_CATALOG[cat]
            method = c_meth.selectbox("Method", meth_options)
            
            # Dynamic Params UI
            params = {}
            st.write("---")
            
            # UI Logic based on Category
            if cat == "1. Structure":
                if method == "Reorder Columns":
                    params["order"] = st.multiselect("Drag to Reorder", df.columns, default=df.columns)
                elif method == "View Info":
                    st.write(df.dtypes)
                    
            elif cat == "2. Creation":
                c1, c2 = st.columns(2)
                params["col_name"] = c1.text_input("New Column Name", "new_col")
                if method == "Create Constant":
                    params["value"] = c2.text_input("Value", "0")
                elif method == "Duplicate Column":
                    params["source_col"] = c2.selectbox("Source Column", df.columns)
                    
            elif cat == "3. Removal":
                if method == "Drop Columns":
                    params["cols"] = st.multiselect("Select Columns to Drop", df.columns)
                    
            elif cat == "4. Renaming":
                if method == "Rename Single":
                    c1, c2 = st.columns(2)
                    params["old_name"] = c1.selectbox("Old Name", df.columns)
                    params["new_name"] = c2.text_input("New Name")
                    
            elif cat == "5. Data Types":
                params["col"] = st.selectbox("Target Column", df.columns, key="type_col")
                if method == "Cast Type":
                    params["type"] = st.selectbox("To Type", ["int", "float", "str", "bool"])
                    
            elif cat == "6. Missing (Col-level)":
                params["col"] = st.selectbox("Target Column", df.columns, key="miss_col_single")
                if "Fill" in method:
                    params["value"] = st.text_input("Fill Value", "0")
                    
            elif cat == "7. Value Cleaning":
                params["col"] = st.selectbox("Target Column", df.columns, key="clean_col")
                if method == "Replace Value":
                    c1, c2 = st.columns(2)
                    params["old_val"] = c1.text_input("Old Value")
                    params["new_val"] = c2.text_input("New Value")
                    
            elif cat == "8. Filtering":
                params["col"] = st.selectbox("Target Column", df.columns, key="filt_col")
                if method == "Filter by Value":
                    params["value"] = st.text_input("Value to match")
                elif method == "Filter by Condition (Range)":
                    c1, c2 = st.columns(2)
                    params["min"] = c1.number_input("Min Value", value=None)
                    params["max"] = c2.number_input("Max Value", value=None)
    
            elif cat == "9. Sorting":
                 params["col"] = st.selectbox("Sort by Column", df.columns)
                 
            elif cat == "10. Deduplication":
                params["cols"] = st.multiselect("Subset Columns (Empty = All)", df.columns)
                
            elif cat == "11. Validation":
                 col = st.selectbox("Inspect Column", df.columns)
                 if col:
                     st.write(f"Unique Values: {df[col].nunique()}")
                     if pd.api.types.is_numeric_dtype(df[col]):
                         st.write(f"Min: {df[col].min()} | Max: {df[col].max()}")
                         
            # Apply Button
            if method != "View Info" and cat != "11. Validation":
                if st.button("⚡ Apply Operation", type="primary"):
                    try:
                        df_new = apply_column_operation(df, cat, method, **params)
                        # Diff check
                        diff_rows = len(df) - len(df_new)
                        diff_cols = len(df.columns) - len(df_new.columns)
                        
                        if diff_rows > 0: st.info(f"Removed {diff_rows} rows.")
                        if diff_cols != 0: st.info(f"Changed {diff_cols} columns.")
                        
                        DataManager.save_dataset(df_new, dataset_name, version_note=f"col_op_{method[:5]}", action_description=f"Applied {method} ({cat})")
                        st.session_state["cloud_datasets"][st.session_state["active_dataset"]] = df_new
                        st.success("Operation Applied!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Operation Failed: {e}")
    
    # ---------------------------------------------------------
    # 3. MISSING VALUES (Conditionally Rendered)
    # ---------------------------------------------------------
    if has_missing:
        # ---------------------------------------------------------
        # 3. ADVANCED MISSING VALUE ENGINE (70+ Techniques)
        # ---------------------------------------------------------
        from .imputation_strategies import IMPUTATION_CATALOG, apply_imputation
        
        with st.expander("🧩 Advanced Missing Value Imputation", expanded=False):
            missing = df.isnull().sum()[lambda x: x > 0]
            if missing.empty:
                st.success("No missing values detected! 🎉")
            else:
                st.write("### Missingness Report")
                st.dataframe(missing.to_frame("Count").T)
                
                c_sel, c_cat = st.columns(2)
                
                # 1. Select Columns
                cols_miss = c_sel.multiselect("Select Target Columns", missing.index, default=missing.index, key="adv_miss_cols")
                
                # 2. Select Category
                cat_options = list(IMPUTATION_CATALOG.keys())
                category = c_cat.selectbox("Imputation Category", cat_options, key="adv_miss_cat")
                
                # 3. Select Method & Params
                methods = IMPUTATION_CATALOG[category]
                
                p_meth, p_conf = st.columns(2)
                method = p_meth.selectbox("Technique", methods, key="adv_miss_meth")
                
                # Dynamic Params
                params = {}
                if category == "5. Distance-based":
                    params["k"] = p_conf.slider("k Neighbors", 1, 20, 5)
                elif category == "1. Deletion-based" and "Ratio" in method:
                    params["ratio"] = p_conf.slider("Missing Ratio Threshold", 0.1, 1.0, 0.5)
                elif "Rolling" in method:
                    params["window"] = p_conf.slider("Window Size", 1, 20, 3)
                    
                st.info(f"ℹ️ Selected: **{method}**")
                
                if st.button("✨ Apply Imputation", type="primary"):
                    try:
                        with st.spinner("Crunching data..."):
                            df_new = apply_imputation(df, cols_miss, category, method, **params)
                        
                        # Check result
                        remaining = df_new[cols_miss].isnull().sum().sum() if not df_new.empty else 0
                        
                        DataManager.save_dataset(df_new, dataset_name, version_note="adv_impute", action_description=f"Applied {method} to {cols_miss}")
                        st.session_state["cloud_datasets"][st.session_state["active_dataset"]] = df_new
                        
                        if remaining == 0:
                            st.success("✅ All missing values in target columns resolved!")
                        else:
                            st.warning(f"⚠️ {remaining} missing values remain (method might not cover all cases).")
                            
                        st.rerun()
                    except Exception as e:
                        st.error(f"Imputation Failed: {e}")

    # ---------------------------------------------------------
    # 4. ADVANCED OUTLIER MANAGEMENT (Conditionally Rendered)
    # ---------------------------------------------------------
    if num_cols:
        from .outlier_manager import OutlierManager
        
        with st.expander("📈 Advanced Outlier Management (Detect & Handle)", expanded=False):
            # 1. Select Column
            col_out = st.selectbox("Select Target Column", num_cols, key="amu_col")
            
            # 2. Configure Detection
            c_det, c_param = st.columns(2)
            detect_method = c_det.selectbox("Detection Method", ["IQR (Boxplot)", "Z-Score", "Modified Z-Score (MAD)", "Percentile"])
            
            det_params = {}
            if detect_method == "IQR (Boxplot)":
                det_params["k"] = c_param.slider("IQR Multiplier (k)", 1.0, 3.0, 1.5)
            elif "Z-Score" in detect_method:
                det_params["threshold"] = c_param.slider("Threshold (Sigma)", 2.0, 5.0, 3.0)
            elif detect_method == "Percentile":
                det_params["lower_p"] = c_param.slider("Lower Percentile", 0.0, 0.1, 0.01)
                det_params["upper_p"] = c_param.slider("Upper Percentile", 0.9, 1.0, 0.99)
                
            # Preview Button
            if st.button("🔍 Detect Outliers"):
                mask = OutlierManager.detect_outliers(df, col_out, detect_method, **det_params)
                count = mask.sum()
                st.session_state["outlier_mask"] = mask
                st.session_state["outlier_col"] = col_out
                st.session_state["outlier_method"] = detect_method # For label
                st.session_state["outlier_count"] = count # Persistence
                
            # Persistent View (using session state to keep detection active)
            if "outlier_mask" in st.session_state and st.session_state.get("outlier_col") == col_out:
                mask = st.session_state["outlier_mask"]
                count = st.session_state["outlier_count"]
                
                st.divider()
                
                if count == 0:
                    st.success("No outliers detected with current settings.")
                else:
                    st.warning(f"⚠️ Found {count} outliers ({count/len(df):.1%}) in '{col_out}'")
                    
                    # Visual: Boxplot with Hue
                    import plotly.express as px
                    
                    # Create temporary viz dataframe
                    # We limit size for performance if needed, but for now full df
                    viz_df = pd.DataFrame({
                        "Value": df[col_out],
                        "Status": ["Outlier" if x else "Normal" for x in mask]
                    })
                    
                    fig = px.box(viz_df, x="Value", color="Status", 
                                 title=f"Distribution Analysis: {col_out} ({st.session_state.get('outlier_method', '')})",
                                 color_discrete_map={"Outlier": "red", "Normal": "blue"})
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.write("### Handle Outliers")
                    c_h1, c_h2 = st.columns(2)
                    handle_method = c_h1.selectbox("Handling Strategy", 
                        ["Remove Rows", "Cap / Winsorize", "Replace with Mean", "Replace with Median", "Replace with Nearest", "Flag Outliers", "Log Transform"])
                    
                    if st.button("🛠️ Apply Handling"):
                        try:
                            df_new = OutlierManager.handle_outliers(df, col_out, mask, handle_method)
                            
                            # Diff check
                            diff = len(df) - len(df_new)
                            
                            DataManager.save_dataset(df_new, dataset_name, version_note=f"outlier_{handle_method[:3]}", 
                                                    action_description=f"Handled {count} outliers in '{col_out}' using {handle_method}")
                            
                            st.session_state["cloud_datasets"][st.session_state["active_dataset"]] = df_new
                            
                            # Clear state
                            if "outlier_mask" in st.session_state: del st.session_state["outlier_mask"]
                            
                            st.success(f"Applied {handle_method}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error handling outliers: {e}")

    # ---------------------------------------------------------
    # 5. ADVANCED TEXT CLEANING (Conditionally Rendered)
    # ---------------------------------------------------------
    if text_cols:
        from .text_cleaner import TEXT_CLEANING_CATALOG, TextCleaner
        
        with st.expander("📝 Advanced Text Cleaning", expanded=False):
            # 1. Select Column
            col_txt = st.selectbox("Select Text Column", text_cols, key="atc_col")
            
            # 2. Select Category & Method
            c_cat, c_meth = st.columns(2)
            cat = c_cat.selectbox("Cleaning Category", list(TEXT_CLEANING_CATALOG.keys()), key="atc_cat")
            meth_options = TEXT_CLEANING_CATALOG[cat]
            method = c_meth.selectbox("Operation", meth_options, key="atc_meth")
            
            # 3. Dynamic Params & Inspector
            params = {}
            st.write("---")
            
            # Inspection View
            if cat == "1. Inspection":
                stats = TextCleaner.inspect_text_column(df, col_txt)
                st.write("#### 🔎 Column Insights")
                c1, c2, c3 = st.columns(3)
                c1.metric("Rows", stats["Total Rows"])
                c2.metric("Empty/Blank", stats["Empty/Blank"])
                c3.metric("Avg Length", stats["Avg Length"])
                
                st.write("**Sample Values:**")
                st.code(stats["Sample"])
            
            # Parameter Inputs for specific methods
            elif "Replace Substring" in method:
                c1, c2 = st.columns(2)
                params["old"] = c1.text_input("Find (Old Value)")
                params["new"] = c2.text_input("Replace (New Value)")
                
            elif "Remove Symbols (Regex)" in method:
                params["pattern"] = st.text_input("Regex Pattern", r'[^a-zA-Z0-9\s]')
                st.caption("Default removes everything except alphanumeric and spaces.")
    
            # Apply Button
            if cat != "1. Inspection":
                if st.button("🧼 Clean Text"):
                    try:
                        df_new = TextCleaner.apply_text_cleaning(df, col_txt, cat, method, **params)
                        
                        # Diff check
                        diff = len(df) - len(df_new)
                        
                        DataManager.save_dataset(df_new, dataset_name, version_note=f"text_{method[:5]}", 
                                                action_description=f"Applied '{method}' to text column '{col_txt}'")
                        
                        st.session_state["cloud_datasets"][st.session_state["active_dataset"]] = df_new
                        st.success(f"Cleaned '{col_txt}'!")
                        if diff > 0: st.info(f"Removed {diff} rows.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Cleaning Error: {e}")

    # ---------------------------------------------------------
    # 6. DATE/TIME EXTRACTION (Conditionally Rendered)
    # ---------------------------------------------------------
    # ---------------------------------------------------------
    # 6. ADVANCED DATE/TIME OPERATIONS
    # ---------------------------------------------------------
    # Always show if df has columns, as users might want to parse strings to dates
    if not df.empty:
        from .datetime_manager import DATETIME_OPS_CATALOG, apply_datetime_operation
        
        with st.expander("📅 Advanced Date/Time Operations (Parse, Clean, Extract)", expanded=False):
            
            # 1. Select Column
            # Prioritize date columns but allow others for parsing
            all_cols = df.columns.tolist()
            default_ix = 0
            if date_cols:
                # Default to first date col
                try: default_ix = all_cols.index(date_cols[0])
                except: pass
            
            col_dt = st.selectbox("Select Target Column", all_cols, index=default_ix, key="adt_col")
            
            # 2. Select Category & Method
            c_cat, c_meth = st.columns(2)
            cat = c_cat.selectbox("Operation Category", list(DATETIME_OPS_CATALOG.keys()), key="adt_cat")
            meth_options = DATETIME_OPS_CATALOG[cat]
            method = c_meth.selectbox("Method", meth_options, key="adt_meth")
            
            # 3. Dynamic Params
            params = {}
            st.write("---")
            
            # UI Logic for Params
            if cat == "1. Inspection":
                 if method == "View Sample Values":
                     st.write(df[col_dt].head(10))
                     st.write(df[col_dt].describe())
                 elif method == "Check Timezone Info":
                     try:
                         if pd.api.types.is_datetime64_any_dtype(df[col_dt]):
                              st.write(f"Timezone: {df[col_dt].dt.tz}")
                         else:
                              st.warning("Not a datetime column.")
                     except Exception as e:
                         st.write(f"Error checking timezone: {e}")

            elif cat == "2. Parsing & Conversion":
                if "Format" in method:
                     params["format"] = st.text_input("Format String (e.g., %Y-%m-%d)", "%Y-%m-%d")
                elif "Unix" in method:
                     params["unit"] = st.selectbox("Unit", ["s", "ms", "ns", "D"], index=0)

            elif cat == "3. Missing & Invalid":
                 if "Constant" in method:
                      params["value"] = st.text_input("Fill Value (Date String)", "2020-01-01")
                 elif "Invalid" in method:
                      # Implicit logic in manager, usually drops or fills
                      pass

            elif cat == "4. Timezone Handling":
                 if "Localize" in method or "Convert" in method:
                      params["tz"] = st.selectbox("Timezone", ["UTC", "US/Pacific", "US/Eastern", "Europe/London", "Asia/Tokyo", "Asia/Kolkata"])
            
            elif cat == "5. Date & Time Validation":
                 if "Past Limit" in method:
                      params["limit_date"] = st.date_input("Limit Date").strftime("%Y-%m-%d")

            elif cat == "8. Comparison & Filtering":
                 if "Before" in method or "After" in method:
                      params["date_val"] = st.date_input("Date Threshold").strftime("%Y-%m-%d")
                 elif "Between" in method:
                      c1, c2 = st.columns(2)
                      params["start_date"] = c1.date_input("Start Date").strftime("%Y-%m-%d")
                      params["end_date"] = c2.date_input("End Date").strftime("%Y-%m-%d")
                 elif "Year" in method:
                      params["year"] = st.number_input("Year", 1900, 2100, 2023)
                 elif "Month" in method:
                      params["month"] = st.slider("Month", 1, 12, 1)

            elif cat == "11. Duration & Diff":
                 if "Difference (vs Column)" in method:
                      params["other_col"] = st.selectbox("Compare with Column", [c for c in df.columns if c != col_dt])

            # Apply Button
            if "View" not in method and "Check" not in method:
                if st.button("📅 Apply Operation"):
                    try:
                        df_new = apply_datetime_operation(df, col_dt, cat, method, **params)
                        
                        # Diff check
                        diff_rows = len(df) - len(df_new)
                        diff_cols = len(df_new.columns) - len(df.columns) # New cols extracted
                        
                        DataManager.save_dataset(df_new, dataset_name, version_note=f"dt_{cat[:3]}", 
                                                action_description=f"Applied {method} on {col_dt}")
                        st.session_state["cloud_datasets"][st.session_state["active_dataset"]] = df_new
                        
                        st.success(f"Applied {method}!")
                        if diff_rows > 0: st.info(f"Dropped {diff_rows} rows.")
                        if diff_cols > 0: st.info(f"Created {diff_cols} new columns.")
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Operation Failed: {e}")
