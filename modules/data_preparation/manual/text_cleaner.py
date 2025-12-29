import pandas as pd
import numpy as np
import re
import streamlit as st

# ---------------------------------------------------------
# CATALOG OVERVIEW
# ---------------------------------------------------------
TEXT_CLEANING_CATALOG = {
    "1. Inspection": ["View Stats & Sample"],
    "2. Missing & Empty": ["Convert NaN to Empty", "Convert Empty to NaN", "Drop Empty Rows"],
    "3. Whitespace": ["Strip All", "Remove Duplicate Spaces", "Normalize Tabs/Newlines"],
    "4. Case Normalization": ["Lower Case", "Upper Case", "Title Case", "Capitalize First"],
    "5. Character Cleaning": ["Remove Punctuation", "Remove Digits", "Remove Non-ASCII", "Remove Symbols (Regex)"],
    "6. Number Handling": ["Remove Numbers", "Keep Only Numbers"],
    "7. Text Normalization": ["Remove Repeated Chars (naive)"],
    "8. Replacement": ["Replace Substring", "Replace with Map"],
    "9. Line Handling": ["Remove Line Breaks", "Replace Breaks with Space"],
    "10. Duplicates": ["Drop Duplicate Text"],
    "11. Validation": ["Identify Short/Long Text"],
    "12. Formatting": ["Trim Final Spaces", "Encoding Fix (UTF-8)"]
}

class TextCleaner:
    
    @staticmethod
    def inspect_text_column(df, col):
        """Returns a dict of inspection stats."""
        series = df[col].astype(str)
        
        # Calculate stats
        n_total = len(series)
        n_empty = series.replace('nan', '').replace('None', '').str.len() == 0
        n_empty_count = n_empty.sum()
        
        lengths = series.str.len()
        avg_len = lengths.mean()
        max_len = lengths.max()
        min_len = lengths.min()
        
        # Sample
        sample = series.head(5).tolist()
        
        return {
            "Total Rows": n_total,
            "Empty/Blank": n_empty_count,
            "Avg Length": f"{avg_len:.1f}",
            "Min/Max Len": f"{min_len} / {max_len}",
            "Sample": sample
        }

    @staticmethod
    def apply_text_cleaning(df, col, category, method, **params):
        """
        Applies text cleaning operation. Returns COPY of df.
        """
        df_new = df.copy()
        
        # Ensure it's string type for operations, except specifically handling mixed
        # But usually we want to work on object cols
        if df_new[col].dtype != "object" and df_new[col].dtype != "string":
             df_new[col] = df_new[col].astype(str)
        
        s = df_new[col]

        # ---------------------------
        # 2. MISSING & EMPTY
        # ---------------------------
        if category == "2. Missing & Empty":
            if method == "Convert NaN to Empty":
                df_new[col] = s.fillna("")
            elif method == "Convert Empty to NaN":
                df_new[col] = s.replace(r'^\s*$', np.nan, regex=True)
            elif method == "Drop Empty Rows":
                # Drops rows where text is empty or whitespace
                mask = s.str.strip().str.len() > 0
                df_new = df_new[mask]

        # ---------------------------
        # 3. WHITESPACE
        # ---------------------------
        elif category == "3. Whitespace":
            if method == "Strip All":
                df_new[col] = s.str.strip()
            elif method == "Remove Duplicate Spaces":
                df_new[col] = s.str.replace(r'\s+', ' ', regex=True)
            elif method == "Normalize Tabs/Newlines":
                df_new[col] = s.str.replace(r'[\t\n\r]+', ' ', regex=True)

        # ---------------------------
        # 4. CASE
        # ---------------------------
        elif category == "4. Case Normalization":
            if method == "Lower Case": df_new[col] = s.str.lower()
            elif method == "Upper Case": df_new[col] = s.str.upper()
            elif method == "Title Case": df_new[col] = s.str.title()
            elif method == "Capitalize First": df_new[col] = s.str.capitalize()

        # ---------------------------
        # 5. CHAR CLEANING
        # ---------------------------
        elif category == "5. Character Cleaning":
            if method == "Remove Punctuation":
                import string
                df_new[col] = s.astype(str).str.translate(str.maketrans('', '', string.punctuation))
            elif method == "Remove Digits":
               df_new[col] = s.astype(str).str.replace(r'\d+', '', regex=True)
            elif method == "Remove Non-ASCII":
               df_new[col] = s.astype(str).str.encode('ascii', 'ignore').str.decode('ascii')
            elif method == "Remove Symbols (Regex)":
               pat = params.get("pattern", r'[^a-zA-Z0-9\s]')
               df_new[col] = s.astype(str).str.replace(pat, '', regex=True)

        # ---------------------------
        # 6. NUMBERS
        # ---------------------------
        elif category == "6. Number Handling":
            if method == "Remove Numbers":
                 df_new[col] = s.astype(str).str.replace(r'\d+', '', regex=True)
            elif method == "Keep Only Numbers":
                 df_new[col] = s.astype(str).str.replace(r'\D+', '', regex=True)

        # ---------------------------
        # 7. NORMALIZATION
        # ---------------------------
        elif category == "7. Text Normalization":
             if method == "Remove Repeated Chars (naive)":
                 # e.g. "goood" -> "god" (too aggressive) or "good"? 
                 # Regex for 3+ same chars -> 1 char: (a)\1+ -> \1
                 df_new[col] = s.astype(str).str.replace(r'(.)\1{2,}', r'\1', regex=True)

        # ---------------------------
        # 8. REPLACEMENT
        # ---------------------------
        elif category == "8. Replacement":
            if method == "Replace Substring":
                old = params.get("old", "")
                new = params.get("new", "")
                df_new[col] = s.astype(str).str.replace(old, new, regex=False)
            elif method == "Replace with Map":
                # Assuming map passed as string "key:val, key2:val2" for UI simplicity
                # Or simplistic map
                pass 

        # ---------------------------
        # 9. LINE HANDLING
        # ---------------------------
        elif category == "9. Line Handling":
            if method == "Remove Line Breaks":
                df_new[col] = s.astype(str).str.replace(r'[\r\n]+', '', regex=True)
            elif method == "Replace Breaks with Space":
                 df_new[col] = s.astype(str).str.replace(r'[\r\n]+', ' ', regex=True)

        # ---------------------------
        # 10. DUPLICATES
        # ---------------------------
        elif category == "10. Duplicates":
            if method == "Drop Duplicate Text":
                df_new = df_new.drop_duplicates(subset=[col])

        # ---------------------------
        # 12. FORMATTING
        # ---------------------------
        elif category == "12. Formatting":
            if method == "Trim Final Spaces":
                df_new[col] = s.astype(str).str.strip() 

        return df_new
