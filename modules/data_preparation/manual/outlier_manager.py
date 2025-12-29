import pandas as pd
import numpy as np
import streamlit as st

class OutlierManager:
    """
    Handles detection and treatment of outliers.
    """
    
    @staticmethod
    def detect_outliers(df, col, method, **params):
        """
        Returns a boolean Series (mask) where True indicates an outlier.
        """
        series = df[col]
        # Ensure numeric
        if not pd.api.types.is_numeric_dtype(series):
            return pd.Series(False, index=df.index)

        # ---------------------------
        # DETECTION METHODS
        # ---------------------------
        if method == "Z-Score":
            threshold = params.get("threshold", 3.0)
            mean = series.mean()
            std = series.std()
            z_scores = (series - mean) / std
            return np.abs(z_scores) > threshold

        elif method == "Modified Z-Score (MAD)":
            threshold = params.get("threshold", 3.5)
            median = series.median()
            median_absolute_deviation = np.median(np.abs(series - median))
            # Avoiding division by zero (if MAD is 0, practically no deviations, unless value != median)
            if median_absolute_deviation == 0:
                 return series != median
            
            # 0.6745 is the consistency constant for normal distribution
            modified_z_scores = 0.6745 * (series - median) / median_absolute_deviation
            return np.abs(modified_z_scores) > threshold

        elif method == "IQR (Boxplot)":
            k = params.get("k", 1.5)
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - (k * IQR)
            upper = Q3 + (k * IQR)
            return (series < lower) | (series > upper)
            
        elif method == "Percentile":
            lower_p = params.get("lower_p", 0.01) # e.g. 1st percentile
            upper_p = params.get("upper_p", 0.99) # e.g. 99th percentile
            lower_val = series.quantile(lower_p)
            upper_val = series.quantile(upper_p)
            return (series < lower_val) | (series > upper_val)

        return pd.Series(False, index=df.index)

    @staticmethod
    def handle_outliers(df, col, mask, method, **params):
        """
        Applies handling strategy to the DataFrame.
        Returns a COPY.
        """
        df_new = df.copy()
        series = df_new[col]
        
        # Some methods (like Transform) don't strictly need the mask, but we pass it for consistency.
        if method == "Log Transform":
             # Shift to positive if needed? 
             # Commonly log1p is used for 0-containing data, or absolute offset for negatives
             min_val = df_new[col].min()
             if min_val <= 0:
                 offset = abs(min_val) + 1
                 df_new[col] = np.log(df_new[col] + offset)
             else:
                 df_new[col] = np.log(df_new[col])
             return df_new

        # For others, we need outliers
        if not mask.any():
            return df_new

        # ---------------------------
        # HANDLING METHODS
        # ---------------------------
        if method == "Remove Rows":
            # Invert mask to keep non-outliers
            df_new = df_new[~mask]
            
        elif method == "Cap / Winsorize":
            # Cap outliers at the boundary of valid data
            valid_min = series[~mask].min()
            valid_max = series[~mask].max()
            
            # Apply capping
            # We must assign to underlying array or loc properly to avoid SettingWithCopy warnings if generic
            df_new.loc[mask & (series < valid_min), col] = valid_min
            df_new.loc[mask & (series > valid_max), col] = valid_max
            
        elif method == "Replace with Mean":
            mean_val = series[~mask].mean()
            df_new.loc[mask, col] = mean_val
            
        elif method == "Replace with Median":
            med_val = series[~mask].median()
            df_new.loc[mask, col] = med_val
        
        elif method == "Replace with Nearest":
            # interpolate nearest? Or just ffill?
            # Nearest is complex for unsorted data. Let's do ffill (Forward Fill) as a proxy for "Nearest Previous"
            df_new.loc[mask, col] = np.nan
            df_new[col] = df_new[col].ffill().bfill()

        elif method == "Flag Outliers":
            df_new[f"{col}_is_outlier"] = mask.astype(int)
            
        return df_new
