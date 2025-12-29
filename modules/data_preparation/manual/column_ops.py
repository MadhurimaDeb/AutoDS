import pandas as pd
import numpy as np

# ---------------------------------------------------------
# CATALOG OVERVIEW
# ---------------------------------------------------------
COLUMN_OPS_CATALOG = {
    "1. Structure": ["View Info", "Reorder Columns"],
    "2. Creation": ["Create Empty", "Create Constant", "Duplicate Column"],
    "3. Removal": ["Drop Columns", "Drop Duplicate Columns"],
    "4. Renaming": ["Rename Single", "Standardize Names (snake_case)"],
    "5. Data Types": ["Cast Type", "Convert String->Date", "Convert Numeric->String"],
    "6. Missing (Col-level)": ["Fill Missing (Const)", "Drop Rows with Missing in Col"],
    "7. Value Cleaning": ["Strip Whitespace", "Replace Value", "Lower Case", "Upper Case"],
    "8. Filtering": ["Filter by Value", "Filter by Condition (Range)"],
    "9. Sorting": ["Sort Ascending", "Sort Descending"],
    "10. Deduplication": ["Drop Duplicates (Subset)"],
    "11. Validation": ["Check Unique/Cardinality"],
    "12. Alignment": ["Show Schema"],
    "13. Export": ["Select Columns for View"]
}

def clean_column_name(name):
    """Standardize column name to snake_case."""
    return str(name).strip().lower().replace(' ', '_').replace('-', '_')

def apply_column_operation(df: pd.DataFrame, category: str, method: str, **params) -> pd.DataFrame:
    """
    Apply column operation based on category and method.
    Returns a COPY of the dataframe.
    """
    df_new = df.copy()
    
    # 1. STRUCTURE
    if category == "1. Structure":
        if method == "Reorder Columns":
            new_order = params.get("order", [])
            # Ensure all original columns are present to avoid data loss
            if set(new_order) == set(df.columns):
                df_new = df_new[new_order]
    
    # 2. CREATION
    elif category == "2. Creation":
        col_name = params.get("col_name", "new_col")
        if method == "Create Empty":
            df_new[col_name] = np.nan
        elif method == "Create Constant":
            val = params.get("value", 0)
            df_new[col_name] = val
        elif method == "Duplicate Column":
            source = params.get("source_col")
            if source in df_new.columns:
                df_new[col_name] = df_new[source]

    # 3. REMOVAL
    elif category == "3. Removal":
        if method == "Drop Columns":
            cols = params.get("cols", [])
            df_new = df_new.drop(columns=cols, errors='ignore')
        elif method == "Drop Duplicate Columns":
            df_new = df_new.T.drop_duplicates().T

    # 4. RENAMING
    elif category == "4. Renaming":
        if method == "Rename Single":
            old = params.get("old_name")
            new = params.get("new_name")
            if old in df_new.columns and new:
                df_new = df_new.rename(columns={old: new})
        elif method == "Standardize Names (snake_case)":
            df_new.columns = [clean_column_name(c) for c in df_new.columns]

    # 5. DATA TYPES
    elif category == "5. Data Types":
        col = params.get("col")
        if col in df_new.columns:
            if method == "Cast Type":
                typ = params.get("type", "str")
                try:
                    df_new[col] = df_new[col].astype(typ)
                except:
                    # Fallback for safe casting
                    if typ == "int": df_new[col] = pd.to_numeric(df_new[col], errors='coerce').fillna(0).astype(int)
                    elif typ == "float": df_new[col] = pd.to_numeric(df_new[col], errors='coerce')
                    else: df_new[col] = df_new[col].astype(str)
            elif method == "Convert String->Date":
                df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
            elif method == "Convert Numeric->String":
                df_new[col] = df_new[col].astype(str)

    # 6. MISSING (COL LEVEL)
    elif category == "6. Missing (Col-level)":
        col = params.get("col")
        if col in df_new.columns:
            if method == "Fill Missing (Const)":
                val = params.get("value", 0)
                df_new[col] = df_new[col].fillna(val)
            elif method == "Drop Rows with Missing in Col":
                df_new = df_new.dropna(subset=[col])

    # 7. VALUE CLEANING
    elif category == "7. Value Cleaning":
        col = params.get("col")
        if col in df_new.columns:
            if method == "Strip Whitespace" and df_new[col].dtype == "object":
                df_new[col] = df_new[col].str.strip()
            elif method == "Lower Case" and df_new[col].dtype == "object":
                df_new[col] = df_new[col].str.lower()
            elif method == "Upper Case" and df_new[col].dtype == "object":
                df_new[col] = df_new[col].str.upper()
            elif method == "Replace Value":
                old_val = params.get("old_val")
                new_val = params.get("new_val")
                df_new[col] = df_new[col].replace(old_val, new_val)

    # 8. FILTERING
    elif category == "8. Filtering":
        col = params.get("col")
        if col in df_new.columns:
            if method == "Filter by Value":
                val = params.get("value")
                df_new = df_new[df_new[col] == val]
            elif method == "Filter by Condition (Range)":
                min_v = params.get("min")
                max_v = params.get("max")
                if min_v is not None: df_new = df_new[df_new[col] >= min_v]
                if max_v is not None: df_new = df_new[df_new[col] <= max_v]

    # 9. SORTING
    elif category == "9. Sorting":
        col = params.get("col")
        if col in df_new.columns:
            asc = (method == "Sort Ascending")
            df_new = df_new.sort_values(by=col, ascending=asc)

    # 10. DEDUPLICATION
    elif category == "10. Deduplication":
        if method == "Drop Duplicates (Subset)":
            cols = params.get("cols", [])
            df_new = df_new.drop_duplicates(subset=cols if cols else None)

    return df_new
