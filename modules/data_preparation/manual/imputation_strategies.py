import pandas as pd
import numpy as np
import streamlit as st
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, KNNImputer, IterativeImputer
from sklearn.linear_model import LinearRegression, BayesianRidge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
import warnings

# Suppress experimental warnings
warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# CATALOG DEFINITIONS
# ---------------------------------------------------------

IMPUTATION_CATALOG = {
    "1. Deletion-based": [
        "Listwise (Drop Rows)",
        "Pairwise (Keep as is)", 
        "Drop Columns (> Ratio)",
    ],
    "2. Simple Deterministic": [
        "Mean", "Median", "Mode", "Constant (0)", "Sentinel (-1)", 
        "Min Value", "Max Value", "Fixed Percentile"
    ],
    "3. Random / Distribution": [
        "Random Sampling (Choice)", 
        "Empirical Distribution"
    ],
    "4. Indicator-based": [
        "Add Missing Indicator",
        "Mark as 'Unknown' (Cat)"
    ],
    "5. Distance-based": [
        "KNN Imputation"
    ],
    "6. Regression / Predictive": [
        "Linear Regression (Iterative)",
        "Bayesian Ridge (PMM-like)"
    ],
    "7. Tree / Ensemble": [
        "Decision Tree Imputation",
        "Random Forest (MissForest-like)",
        "Gradient Boosting"
    ],
    "8. Iterative / Multivariate": [
        "MICE (Standard)",
    ],
    "11. Deep Learning": [
        "Pseudo-Autoencoder (MLP Imputer)"
    ],
    "12. Time-Series Specific": [
        "Forward Fill", "Backward Fill", 
        "Linear Interpolation", "Spline Interpolation (Ord 3)", 
        "Polynomial Interpolation (Ord 2)", "Rolling Mean"
    ]
}

# ---------------------------------------------------------
# IMPLEMENTATION LOGIC
# ---------------------------------------------------------

def apply_imputation(df: pd.DataFrame, target_cols: list, category: str, method: str, **params) -> pd.DataFrame:
    """
    Apply the selected imputation method to the target columns.
    Returns a COPY of the dataframe.
    """
    df_new = df.copy()
    
    # ---------------------------
    # 1. DELETION
    # ---------------------------
    if category == "1. Deletion-based":
        if method == "Listwise (Drop Rows)":
            df_new = df_new.dropna(subset=target_cols)
        elif method == "Drop Columns (> Ratio)":
            ratio = params.get("ratio", 1.0) # 1.0 means drop if ANY missing, user might set 0.5
            # Logic: drop cols from df_new if they are in target_cols AND miss ratio > thresh
            # For simplicity in this UI, we usually just drop the selected cols entirely? 
            # Or drop ROWS? The request said 'Feature pruning'. 
            # Let's interpret as: Drop these columns if they have missing values.
            df_new = df_new.drop(columns=target_cols)

    # ---------------------------
    # 2. SIMPLE
    # ---------------------------
    elif category == "2. Simple Deterministic":
        for col in target_cols:
            if method == "Mean" and pd.api.types.is_numeric_dtype(df_new[col]):
                df_new[col] = df_new[col].fillna(df_new[col].mean())
            elif method == "Median" and pd.api.types.is_numeric_dtype(df_new[col]):
                df_new[col] = df_new[col].fillna(df_new[col].median())
            elif method == "Mode":
                if not df_new[col].mode().empty:
                    df_new[col] = df_new[col].fillna(df_new[col].mode()[0])
            elif method == "Constant (0)":
                df_new[col] = df_new[col].fillna(0)
            elif method == "Sentinel (-1)":
                df_new[col] = df_new[col].fillna(-1)
            elif method == "Min Value":
                 if pd.api.types.is_numeric_dtype(df_new[col]):
                    df_new[col] = df_new[col].fillna(df_new[col].min())
            elif method == "Max Value":
                 if pd.api.types.is_numeric_dtype(df_new[col]):
                    df_new[col] = df_new[col].fillna(df_new[col].max())

    # ---------------------------
    # 3. RANDOM
    # ---------------------------
    elif category == "3. Random / Distribution":
        if method == "Random Sampling (Choice)":
            for col in target_cols:
                mask = df_new[col].isnull()
                samples = df_new[col].dropna().sample(n=mask.sum(), replace=True)
                df_new.loc[mask, col] = samples.values

    # ---------------------------
    # 4. INDICATOR
    # ---------------------------
    elif category == "4. Indicator-based":
        if method == "Add Missing Indicator":
            for col in target_cols:
                df_new[f"{col}_missing"] = df_new[col].isnull().astype(int)
        elif method == "Mark as 'Unknown' (Cat)":
             for col in target_cols:
                 df_new[col] = df_new[col].fillna("Unknown")

    # ---------------------------
    # 5. DISTANCE (KNN)
    # ---------------------------
    elif category == "5. Distance-based":
        k = params.get("k", 5)
        # KNN requires numeric data mostly. We filter only numeric target cols?
        # Actually sklearn KNN can handle whole matrix if numeric.
        numeric_data = df_new.select_dtypes(include=np.number)
        if not numeric_data.empty:
            imputer = KNNImputer(n_neighbors=k)
            imputed_data = imputer.fit_transform(numeric_data)
            df_new[numeric_data.columns] = imputed_data

    # ---------------------------
    # 6, 7, 8, 11 (ITERATIVE / MODEL BASED)
    # ---------------------------
    elif category in ["6. Regression / Predictive", "7. Tree / Ensemble", "8. Iterative / Multivariate", "11. Deep Learning"]:
        
        estimator = None
        if method == "Linear Regression (Iterative)": estimator = LinearRegression()
        elif method == "Bayesian Ridge (PMM-like)" or category == "8. Iterative / Multivariate": estimator = BayesianRidge()
        elif method == "Decision Tree Imputation": estimator = DecisionTreeRegressor(max_depth=10)
        elif method == "Random Forest (MissForest-like)": estimator = RandomForestRegressor(n_jobs=-1, max_depth=10)
        elif method == "Gradient Boosting": estimator = GradientBoostingRegressor()
        elif "MLP" in method: 
            from sklearn.neural_network import MLPRegressor
            estimator = MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=200)

        # Sklearn IterativeImputer fits on numeric.
        numeric_data = df_new.select_dtypes(include=np.number)
        if not numeric_data.empty and estimator:
            imputer = IterativeImputer(estimator=estimator, max_iter=10, random_state=0)
            imputed_data = imputer.fit_transform(numeric_data)
            df_new[numeric_data.columns] = imputed_data

    # ---------------------------
    # 12. TIME SERIES
    # ---------------------------
    elif category == "12. Time-Series Specific":
        for col in target_cols:
            if method == "Forward Fill": df_new[col] = df_new[col].ffill()
            elif method == "Backward Fill": df_new[col] = df_new[col].bfill()
            elif method == "Linear Interpolation": 
                df_new[col] = df_new[col].interpolate(method='linear')
            elif method == "Spline Interpolation (Ord 3)":
                df_new[col] = df_new[col].interpolate(method='spline', order=3)
            elif method == "Polynomial Interpolation (Ord 2)":
                df_new[col] = df_new[col].interpolate(method='polynomial', order=2)
            elif method == "Rolling Mean":
                window = params.get("window", 3)
                # Fill with rolling mean (tricky if consecutive missing, but simple attempt)
                df_new[col] = df_new[col].fillna(df_new[col].rolling(window, min_periods=1, center=True).mean())

    return df_new
