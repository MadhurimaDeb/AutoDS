import pandas as pd
import numpy as np

# ---------------------------------------------------------
# DATETIME CATALOG
# ---------------------------------------------------------
DATETIME_OPS_CATALOG = {
    "1. Inspection": [
        "View Sample Values", 
        "Check Timezone Info"
    ],
    "2. Parsing & Conversion": [
        "Convert String to Datetime (Auto)",
        "Convert String to Datetime (Format)",
        "Convert Unix Timestamp to Datetime",
        "Convert Datetime to String (Format)"
    ],
    "3. Missing & Invalid": [
        "Fill Missing (Constant)", 
        "Fill Missing (Forward Fill)", 
        "Fill Missing (Backward Fill)",
        "Drop Rows with Missing Datetime"
    ],
    "4. Timezone Handling": [
        "Localize Timezone (Naive -> Aware)",
        "Convert Timezone",
        "Remove Timezone (Make Naive)"
    ],
    "5. Date & Time Validation": [
        "Filter Invalid Dates (Future)",
        "Filter Invalid Dates (Past Limit)"
    ],
    "6. Formatting": [
        "Standardize Format (ISO8601)",
        "Round to Day (Remove Time)",
        "Round to Minute (Remove Seconds)"
    ],
    "7. Extraction": [
        "Extract Year", "Extract Month", "Extract Day",
        "Extract Hour", "Extract Minute", "Extract Second",
        "Extract Weekday Name"
    ],
    "8. Comparison & Filtering": [
        "Filter Before Date",
        "Filter After Date",
        "Filter Between Dates",
        "Filter by Year",
        "Filter by Month"
    ],
    "9. Sorting": [
        "Sort Chronological (Asc)",
        "Sort Reverse Chronological (Desc)"
    ],
    "10. Duplicates": [
        "Drop Duplicate Timestamps"
    ],
    "11. Duration & Diff": [
        "Compute Time Since (Now)",
        "Compute Difference (vs Column)"
    ],
    "12. Alignment": [
        "Align Timezone (to UTC)"
    ],
    "13. Export Prep": [
        "Convert to String (ISO for Export)"
    ]
}

def apply_datetime_operation(df: pd.DataFrame, col: str, category: str, method: str, **params) -> pd.DataFrame:
    """
    Apply datetime operation on a specific column.
    Returns a COPY of the dataframe.
    """
    df_new = df.copy()
    
    # Validation: Ensure column exists
    if col not in df_new.columns:
        return df_new

    # ---------------------------
    # 2. Parsing & Conversion
    # ---------------------------
    if category == "2. Parsing & Conversion":
        if method == "Convert String to Datetime (Auto)":
            df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
            
        elif method == "Convert String to Datetime (Format)":
            fmt = params.get("format", "%Y-%m-%d")
            df_new[col] = pd.to_datetime(df_new[col], format=fmt, errors='coerce')
            
        elif method == "Convert Unix Timestamp to Datetime":
            unit = params.get("unit", "s")
            df_new[col] = pd.to_datetime(df_new[col], unit=unit, errors='coerce')
            
        elif method == "Convert Datetime to String (Format)":
            fmt = params.get("format", "%Y-%m-%d")
            # Only works if col is already datetime
            if pd.api.types.is_datetime64_any_dtype(df_new[col]):
                df_new[col] = df_new[col].dt.strftime(fmt)

    # ---------------------------
    # 3. Missing & Invalid
    # ---------------------------
    elif category == "3. Missing & Invalid":
        if method == "Fill Missing (Constant)":
            # For datetime, constant usually implies a specific date
            val = params.get("value") # Expecting string or datetime
            df_new[col] = df_new[col].fillna(pd.to_datetime(val))
            
        elif method == "Fill Missing (Forward Fill)":
            df_new[col] = df_new[col].ffill()
            
        elif method == "Fill Missing (Backward Fill)":
            df_new[col] = df_new[col].bfill()
            
        elif method == "Drop Rows with Missing Datetime":
            df_new = df_new.dropna(subset=[col])

    # ---------------------------
    # 4. Timezone Handling
    # ---------------------------
    elif category == "4. Timezone Handling":
        # Ensure dt accessor
        if not pd.api.types.is_datetime64_any_dtype(df_new[col]):
             df_new[col] = pd.to_datetime(df_new[col], errors='coerce')

        if method == "Localize Timezone (Naive -> Aware)":
            tz = params.get("tz", "UTC")
            # IF already localized, this might fail, so we can convert or localize
            if df_new[col].dt.tz is None:
                df_new[col] = df_new[col].dt.tz_localize(tz)
            else:
                 df_new[col] = df_new[col].dt.tz_convert(tz)

        elif method == "Convert Timezone":
            tz = params.get("tz", "UTC")
            if df_new[col].dt.tz is None:
                # If naive, localize first
                 df_new[col] = df_new[col].dt.tz_localize('UTC')
            df_new[col] = df_new[col].dt.tz_convert(tz)

        elif method == "Remove Timezone (Make Naive)":
            df_new[col] = df_new[col].dt.tz_localize(None)

    # ---------------------------
    # 5. Date & Time Validation
    # ---------------------------
    elif category == "5. Date & Time Validation":
        if not pd.api.types.is_datetime64_any_dtype(df_new[col]):
             df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
             
        now = pd.Timestamp.now()
        if method == "Filter Invalid Dates (Future)":
            df_new = df_new[df_new[col] <= now]
        elif method == "Filter Invalid Dates (Past Limit)":
            limit = pd.to_datetime(params.get("limit_date", "1900-01-01"))
            df_new = df_new[df_new[col] >= limit]

    # ---------------------------
    # 6. Formatting (Updates values or Type)
    # ---------------------------
    elif category == "6. Formatting":
        if not pd.api.types.is_datetime64_any_dtype(df_new[col]):
             df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
             
        if method == "Standardize Format (ISO8601)":
             # Converts to string ISO format
             df_new[col] = df_new[col].dt.strftime('%Y-%m-%dT%H:%M:%S')
             
        elif method == "Round to Day (Remove Time)":
            df_new[col] = df_new[col].dt.normalize()
            
        elif method == "Round to Minute (Remove Seconds)":
            df_new[col] = df_new[col].dt.floor('Min')

    # ---------------------------
    # 7. Extraction
    # ---------------------------
    elif category == "7. Extraction":
        # Extract creates a NEW column
        if not pd.api.types.is_datetime64_any_dtype(df_new[col]):
             df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
             
        suffix = method.split(" ")[1] # e.g. Year, Month
        new_col_name = f"{col}_{suffix}"
        
        if method == "Extract Year": df_new[new_col_name] = df_new[col].dt.year
        elif method == "Extract Month": df_new[new_col_name] = df_new[col].dt.month
        elif method == "Extract Day": df_new[new_col_name] = df_new[col].dt.day
        elif method == "Extract Hour": df_new[new_col_name] = df_new[col].dt.hour
        elif method == "Extract Minute": df_new[new_col_name] = df_new[col].dt.minute
        elif method == "Extract Second": df_new[new_col_name] = df_new[col].dt.second
        elif method == "Extract Weekday Name": df_new[new_col_name] = df_new[col].dt.day_name()

    # ---------------------------
    # 8. Comparison & Filtering
    # ---------------------------
    elif category == "8. Comparison & Filtering":
        if not pd.api.types.is_datetime64_any_dtype(df_new[col]):
             df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
             
        if method == "Filter Before Date":
            date_val = pd.to_datetime(params.get("date_val"))
            df_new = df_new[df_new[col] < date_val]
        elif method == "Filter After Date":
            date_val = pd.to_datetime(params.get("date_val"))
            df_new = df_new[df_new[col] > date_val]
        elif method == "Filter Between Dates":
            start = pd.to_datetime(params.get("start_date"))
            end = pd.to_datetime(params.get("end_date"))
            df_new = df_new[(df_new[col] >= start) & (df_new[col] <= end)]
        elif method == "Filter by Year":
            year = int(params.get("year"))
            df_new = df_new[df_new[col].dt.year == year]
        elif method == "Filter by Month":
            month = int(params.get("month"))
            df_new = df_new[df_new[col].dt.month == month]

    # ---------------------------
    # 9. Sorting
    # ---------------------------
    elif category == "9. Sorting":
         if method == "Sort Chronological (Asc)":
             df_new = df_new.sort_values(by=col, ascending=True)
         elif method == "Sort Reverse Chronological (Desc)":
             df_new = df_new.sort_values(by=col, ascending=False)

    # ---------------------------
    # 10. Duplicates
    # ---------------------------
    elif category == "10. Duplicates":
        # Keep first occurrence
        df_new = df_new.drop_duplicates(subset=[col])

    # ---------------------------
    # 11. Duration & Diff
    # ---------------------------
    elif category == "11. Duration & Diff":
        if not pd.api.types.is_datetime64_any_dtype(df_new[col]):
             df_new[col] = pd.to_datetime(df_new[col], errors='coerce')
             
        if method == "Compute Time Since (Now)":
            now = pd.Timestamp.now()
            # If TZ aware, make now aware usually logic needs match
            if df_new[col].dt.tz is not None:
                now = pd.Timestamp.now(tz=df_new[col].dt.tz)
            df_new[f"{col}_days_since"] = (now - df_new[col]).dt.days
        
        elif method == "Compute Difference (vs Column)":
            other_col = params.get("other_col")
            if other_col in df_new.columns:
                 df_new[f"{col}_diff_{other_col}"] = df_new[col] - pd.to_datetime(df_new[other_col], errors='coerce')

    # ---------------------------
    # 12. Alignment
    # ---------------------------
    elif category == "12. Alignment":
        if method == "Align Timezone (to UTC)":
             if df_new[col].dt.tz is None:
                 df_new[col] = df_new[col].dt.tz_localize('UTC')
             else:
                 df_new[col] = df_new[col].dt.tz_convert('UTC')

    # ---------------------------
    # 13. Export Prep
    # ---------------------------
    elif category == "13. Export Prep":
         if method == "Convert to String (ISO for Export)":
             # Force convert to string formatted ISO
             # Safe check if it's datetime
             if pd.api.types.is_datetime64_any_dtype(df_new[col]):
                df_new[col] = df_new[col].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
             else:
                 # Try parsing then reformatting
                 try:
                     df_new[col] = pd.to_datetime(df_new[col]).dt.strftime('%Y-%m-%dT%H:%M:%S%z')
                 except:
                     pass

    return df_new
