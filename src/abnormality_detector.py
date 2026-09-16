import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
try:
    from .simulate_randles import randles_impedance
    from .feature_engineering import extract_features
except ImportError:
    from simulate_randles import randles_impedance
    from feature_engineering import extract_features

def simulate_safe_proxy_faults(n_samples=200):
    """
    Simulate impedance of 'Normal' cells vs cells with an 'RC-proxy fault'.
    The literature often uses an external RC circuit in parallel with the cell 
    to safely emulate an internal short circuit (ISC) without destructive thermal runaway.
    
    This function generates synthetic features for both cases.
    """
    frequencies = np.logspace(-2, 3, 20)
    data = []
    
    for i in range(n_samples):
        # Base healthy variation
        R0 = np.random.uniform(0.04, 0.06)
        Rct = np.random.uniform(0.08, 0.15)
        Cdl = np.random.uniform(0.4, 0.6)
        
        is_fault = (i % 2 == 0) # 50/50 split
        
        if is_fault:
            # Emulating an external proxy resistance in parallel: R_proxy
            # This significantly reduces overall low-frequency impedance
            R_proxy = np.random.uniform(0.5, 2.0)
            # Parallel equation roughly applied to Rct for demonstration
            Rct = 1.0 / ( (1.0/Rct) + (1.0/R_proxy) )
            label = 1
        else:
            label = 0
            
        # Simulate ideal impedance
        Z = randles_impedance(frequencies, R0, Rct, Cdl, sigma=0.01)
        
        # Add sensor noise
        noise = np.random.normal(0, 0.005, len(Z)) + 1j*np.random.normal(0, 0.005, len(Z))
        Z += noise
        
        # Extract features
        features = extract_features(frequencies, Z)
        features['Is_Fault'] = label
        data.append(features)
        
    return pd.DataFrame(data)

def train_abnormality_detector(df):
    """
    Train a Random Forest classifier to detect the RC-proxy simulated fault.
    """
    X = df[['R_ohm_est', 'R_pol_est', 'Max_Img_Z', 'Z_mag_1Hz', 'Phase_10Hz']]
    y = df['Is_Fault']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)
    
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    
    # print(classification_report(y_test, preds))
    return clf, acc

if __name__ == "__main__":
    df = simulate_safe_proxy_faults()
    model, acc = train_abnormality_detector(df)
    print(f"Abnormality Detector Accuracy: {acc*100:.2f}%")
