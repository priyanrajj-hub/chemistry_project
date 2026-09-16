import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from dft_extraction import extract_impedance_dft, generate_signals
from simulate_randles import randles_impedance

def test_dft_extraction_accuracy():
    """
    Test that the single-bin DFT correctly extracts the complex impedance
    from the generated noisy time-domain signals.
    """
    f_stimulus = 10.0 # 10 Hz
    # Some true impedance
    Z_true = 0.1 - 0.05j 
    
    t, v, i = generate_signals(f_stimulus, Z_true, sampling_rate=860, duration=1.0, noise_std=0.001)
    
    Z_est = extract_impedance_dft(f_stimulus, t, v, i)
    
    # Should be within reasonable tolerance despite noise
    assert np.abs(np.real(Z_true) - np.real(Z_est)) < 0.01, f"Real part mismatch: {np.real(Z_true)} vs {np.real(Z_est)}"
    assert np.abs(np.imag(Z_true) - np.imag(Z_est)) < 0.01, f"Imag part mismatch: {np.imag(Z_true)} vs {np.imag(Z_est)}"

def test_randles_simulation():
    """
    Test the randles circuit physics constraint (low freq => higher real resistance).
    """
    freqs = np.array([1000.0, 0.1])
    Z = randles_impedance(freqs, R0=0.05, Rct=0.2, Cdl=0.5, sigma=0.0)
    
    # High freq intercept should be approx R0
    assert np.abs(np.real(Z[0]) - 0.05) < 0.05 
    
    # Low freq intercept should be approx R0 + Rct
    assert np.abs(np.real(Z[1]) - 0.25) < 0.05 

if __name__ == "__main__":
    test_dft_extraction_accuracy()
    test_randles_simulation()
    print("All basic unit tests passed!")
