import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add current dir to path to allow absolute imports when running as module
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from simulate_randles import generate_soh_profiles
from dft_extraction import sweep_frequencies
from nasa_dataset_loader import get_nasa_dataset
from feature_engineering import extract_features
from soh_model import train_soh_model
from abnormality_detector import simulate_safe_proxy_faults, train_abnormality_detector

import json

def plot_nyquist_bode(frequencies, profiles):
    """Generate and save standard EIS visualizations."""
    os.makedirs('figures', exist_ok=True)
    
    # Use dark background for premium website look
    plt.style.use('dark_background')
    
    # Dump data for the 3D Plotly integration
    json_data = {'frequencies': frequencies.tolist(), 'series': {}}
    
    # 1. Nyquist Plot
    plt.figure(figsize=(8, 6))
    colors = {'Fresh': '#00ffc8', 'Mid-life': '#028090', 'Aged': '#ff4d4d'}
    
    for state, Z in profiles.items():
        # Extracted via software DFT pipeline to prove it works
        Z_est = sweep_frequencies(frequencies, Z, sampling_rate=860)
        plt.plot(np.real(Z_est), -np.imag(Z_est), 'o-', markersize=4, label=f"{state}", color=colors[state])
        
        # Save to json dict for JS
        json_data['series'][state] = {
            'z_real': np.real(Z_est).tolist(),
            'z_imag': (-np.imag(Z_est)).tolist() # negate imag for standard Nyquist convention
        }
        
    # Write json data
    with open('nyquist_data.json', 'w') as f:
        json.dump(json_data, f)
        
    plt.title('Nyquist Plot of Battery Aging')
    plt.xlabel("Z' (\u03A9)")
    plt.ylabel("-Z'' (\u03A9)")
    plt.legend()
    plt.grid(True, color='#222222', linestyle=':')
    
    # Ensure axes are equal for proper Nyquist representation
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.savefig('figures/nyquist_plot.png', dpi=300, facecolor='#0a0e17')
    plt.close()
    
    # 2. Bode Plot (Magnitude)
    plt.figure(figsize=(8, 6))
    for state, Z in profiles.items():
        Z_est = sweep_frequencies(frequencies, Z)
        plt.semilogx(frequencies, np.abs(Z_est), 's-', markersize=4, label=state, color=colors[state])
        
    plt.title('Bode Plot (Magnitude)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('|Z| (\u03A9)')
    plt.legend()
    plt.grid(True, color='#222222', linestyle=':')
    plt.tight_layout()
    plt.savefig('figures/bode_magnitude.png', dpi=300, facecolor='#0a0e17')
    plt.close()

def plot_capacity_fade(nasa_df):
    plt.figure(figsize=(8, 5))
    plt.plot(nasa_df['Cycle'], nasa_df['Capacity_Ah'], color='#00ffc8', linewidth=2)
    plt.title('NASA Li-ion Dataset: Capacity Fade')
    plt.xlabel('Cycle')
    plt.ylabel('Capacity (Ah)')
    plt.grid(True, color='#222222', linestyle=':')
    plt.tight_layout()
    plt.savefig('figures/capacity_fade.png', dpi=300, facecolor='#0a0e17')
    plt.close()

def run():
    print("--- Low-Cost EIS Pipeline Execution ---")
    
    # Step 1: Simulate Impedance and DFT pipeline
    print("1. Running DFT extractions and generating Nyquist/Bode plots...")
    freqs = np.logspace(-2, 3, 30) # 0.01 Hz to 1000 Hz
    profiles = generate_soh_profiles(freqs)
    plot_nyquist_bode(freqs, profiles)
    
    # Step 2: NASA Dataset and Feature Engineering
    print("2. Generating baseline dataset and simulating Hardware Feature Extraction...")
    df = get_nasa_dataset()
    plot_capacity_fade(df)
    
    # We will simulate the DFT extraction step for every cycle's true params
    # We do a simplified approach here rather than running the time-series sim for 160 cycles due to speed
    # We'll just generate the true Z and add noise, then extract features.
    
    extracted_features_list = []
    for idx, row in df.iterrows():
        # using our simulate functionality on the true values
        from simulate_randles import randles_impedance
        Z_true = randles_impedance(freqs, row['R0_True'], row['Rct_True'], row['Cdl_True'], sigma=0.01)
        
        # simulated extraction noise (representing cheap sensors)
        Z_est = Z_true + np.random.normal(0, 0.002, len(freqs)) + 1j*np.random.normal(0, 0.002, len(freqs))
        
        feat = extract_features(freqs, Z_est)
        feat['SoH'] = row['SoH']
        extracted_features_list.append(feat)
        
    features_df = pd.DataFrame(extracted_features_list)
    
    # Step 3: Train SoH Model
    print("3. Training Random Forest Regressor for SoH Prediction...")
    model, metrics = train_soh_model(features_df)
    print("\n   [Model Metrics]")
    print(f"   RF MAE:  {metrics['RF_MAE']:.4f}")
    print(f"   RF RMSE: {metrics['RF_RMSE']:.4f}")
    print(f"   RF R²:   {metrics['RF_R2']:.4f}\n")
    
    # Step 4: Abnormality Detection (Safe RC Proxy)
    print("4. Training Abnormality Classifier (RC Proxy Faults)...")
    anomaly_df = simulate_safe_proxy_faults()
    clf, acc = train_abnormality_detector(anomaly_df)
    print(f"   Classifier Accuracy: {acc*100:.2f}%\n")
    
    print("--- Pipeline Complete. Check 'figures/' directory. ---")

if __name__ == "__main__":
    run()
