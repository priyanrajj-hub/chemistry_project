import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os

def train_soh_model(features_df):
    """
    Train a Random Forest Regressor and a baseline Linear Regression 
    to predict State of Health (SoH) based on extracted impedance features.
    
    features_df must contain the extracted features and a 'SoH' column.
    """
    feature_cols = ['R_ohm_est', 'R_pol_est', 'Max_Img_Z', 'Z_mag_1Hz', 'Phase_10Hz']
    
    X = features_df[feature_cols]
    y = features_df['SoH']
    
    # Standard 80/20 train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Baseline Model
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_preds = lr.predict(X_test)
    
    # 2. Main Model (Random Forest)
    rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    
    # Metrics
    metrics = {
        'Baseline_R2': r2_score(y_test, lr_preds),
        'Baseline_MAE': mean_absolute_error(y_test, lr_preds),
        'Baseline_RMSE': np.sqrt(mean_squared_error(y_test, lr_preds)),
        
        'RF_R2': r2_score(y_test, rf_preds),
        'RF_MAE': mean_absolute_error(y_test, rf_preds),
        'RF_RMSE': np.sqrt(mean_squared_error(y_test, rf_preds)),
    }
    
    # Generate and save Plot
    plt.style.use('dark_background')
    os.makedirs('figures', exist_ok=True)
    plt.figure(figsize=(8, 6))
    
    # Sort for cleaner line plotting if treating as a timeseries, 
    # but since it's a scatter plot, we just plot Pred vs Actual.
    plt.scatter(y_test, rf_preds, alpha=0.7, color='#00ffc8', label='RF Predictions', edgecolor='none')
    
    # Perfect prediction line
    min_val = min(y_test.min(), rf_preds.min())
    max_val = max(y_test.max(), rf_preds.max())
    plt.plot([min_val, max_val], [min_val, max_val], '--', color='#ff4d4d', label='Perfect Fit')
    
    plt.title('Predicted vs Reference SoH (Random Forest)')
    plt.xlabel('Reference SoH (Capacity based)')
    plt.ylabel('Predicted SoH')
    plt.legend()
    plt.grid(True, color='#222222', linestyle=':')
    
    plt.text(min_val + 0.05*(max_val-min_val), max_val - 0.1*(max_val-min_val),
             f"MAE:  {metrics['RF_MAE']:.4f}\n"
             f"RMSE: {metrics['RF_RMSE']:.4f}\n"
             f"R²:   {metrics['RF_R2']:.4f}",
             bbox=dict(facecolor='#111111', alpha=0.9, edgecolor='#00ffc8'))
             
    plt.tight_layout()
    plt.savefig('figures/predicted_vs_reference_soh.png', dpi=300, facecolor='#0a0e17')
    plt.close()
    
    return rf, metrics
