import os
import pandas as pd
import numpy as np

def get_nasa_dataset():
    """
    Simulates loading the NASA PCoE Li-ion Aging Dataset.
    In a real scenario, this would parse the MATLAB files from:
    https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/
    
    Since downloading and parsing the full dataset in a CI/CD or demo
    environment is heavy and error-prone, we generate a synthetic representative
    subset that mimics actual battery aging (Capacity fade over cycles).
    """
    os.makedirs('data/sample', exist_ok=True)
    sample_path = 'data/sample/nasa_battery_sample.csv'
    
    if os.path.exists(sample_path):
        return pd.read_csv(sample_path)
    
    # Generate realistic pseudo-data representing battery cycling
    # NASA dataset typically shows capacity degrading from ~2.0 Ah to ~1.4 Ah over ~160 cycles.
    cycles = np.arange(1, 161)
    
    # Base capacity fade with some noise and non-linearity
    start_cap = 2.05
    end_cap = 1.38
    
    # Exponential decay shape
    capacity = start_cap - (start_cap - end_cap) * ((cycles) / max(cycles))**1.5
    capacity += np.random.normal(0, 0.015, len(cycles))
    
    # SoH is directly proportional to remaining capacity
    soh = capacity / start_cap
    
    # Associated simplified Impedance parameters that shift as SoH drops
    # Usually: R0 rises slowly, Rct rises exponentially.
    R0 = 0.05 + 0.06 * (1 - soh)
    R0 += np.random.normal(0, 0.002, len(cycles))
    
    Rct = 0.08 + 0.5 * (1 - soh)**2
    Rct += np.random.normal(0, 0.01, len(cycles))
    
    Cdl = 0.5 - 0.2 * (1 - soh)
    Cdl += np.random.normal(0, 0.02, len(cycles))
    
    df = pd.DataFrame({
        'Cycle': cycles,
        'Capacity_Ah': capacity,
        'SoH': soh,
        'R0_True': R0,
        'Rct_True': Rct,
        'Cdl_True': Cdl
    })
    
    df.to_csv(sample_path, index=False)
    print(f"Created cached representative dataset at {sample_path}")
    return df
    
if __name__ == "__main__":
    df = get_nasa_dataset()
    print(df.head())
