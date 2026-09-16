import numpy as np

def randles_impedance(frequencies, R0, Rct, Cdl, sigma=0.0):
    """
    Simulates the complex impedance Z(w) of a simplified Randles circuit.
    Model: Z(w) = R0 + Z_parallel + Z_Warburg
    Where Z_parallel is Rct || (1 / j*w*Cdl)
    Since this is a low-frequency demonstrator, we'll model Z_Warburg 
    simply as sigma * (1-j) / sqrt(w), or set it to 0 if sigma=0.

    Parameters:
    -----------
    frequencies : array-like
        Frequencies in Hz.
    R0 : float
        Ohmic resistance (series).
    Rct : float
        Charge transfer resistance.
    Cdl : float
        Double layer capacitance.
    sigma : float
        Warburg coefficient (simplified).

    Returns:
    --------
    Z : np.ndarray
        Array of complex impedance values at the given frequencies.
    """
    w = 2 * np.pi * np.array(frequencies)
    
    # Warburg impedance component (simplified)
    # Avoid zero division
    w_safe = np.where(w == 0, 1e-10, w)
    Z_W = sigma * (1 - 1j) / np.sqrt(w_safe)
    
    # Parallel RC component
    # Z_parallel = 1 / ((1 / Rct) + j*w*Cdl)
    Z_parallel = 1.0 / ( (1.0 / Rct) + 1j * w * Cdl )
    
    # Total impedance
    Z = R0 + Z_parallel + Z_W
    
    return Z

def generate_soh_profiles(frequencies):
    """
    Generate synthetic impedance spectra for Fresh, Mid-life, and Aged batteries.
    Values are purely illustrative for the demonstrator.
    """
    # Fresh battery: Low R0, Low Rct
    Z_fresh = randles_impedance(frequencies, R0=0.05, Rct=0.1, Cdl=0.5, sigma=0.01)
    
    # Mid-life battery: Slightly increased R0 and Rct
    Z_mid = randles_impedance(frequencies, R0=0.08, Rct=0.25, Cdl=0.4, sigma=0.015)
    
    # Aged battery: Significantly increased R0 and Rct
    Z_aged = randles_impedance(frequencies, R0=0.15, Rct=0.6, Cdl=0.3, sigma=0.02)
    
    return {
        'Fresh': Z_fresh,
        'Mid-life': Z_mid,
        'Aged': Z_aged
    }

if __name__ == "__main__":
    freqs = np.logspace(-2, 3, 50)
    profiles = generate_soh_profiles(freqs)
    print("Generated 50-point spectra for Fresh, Mid-life, Aged.")
