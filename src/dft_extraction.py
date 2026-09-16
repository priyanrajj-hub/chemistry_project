import numpy as np

def generate_signals(f_stimulus, Z_actual, sampling_rate=860, duration=1.0, noise_std=0.01):
    """
    Generate synthetic time-domain voltage and current signals given a stimulus frequency.
    Simulates ADC (e.g. max 860 SPS for ADS1115).
    """
    t = np.arange(0, duration, 1.0 / sampling_rate)
    
    # Original current sine wave (stimulus)
    I_amp = 1.0
    i_signal = I_amp * np.sin(2 * np.pi * f_stimulus * t)
    
    # Voltage response based on complex Z (magnitude and phase)
    mag_Z = np.abs(Z_actual)
    phase_Z = np.angle(Z_actual)
    v_signal = I_amp * mag_Z * np.sin(2 * np.pi * f_stimulus * t + phase_Z)
    
    # Add noise corresponding to cheap sensor quality
    i_signal += np.random.normal(0, noise_std, len(t))
    v_signal += np.random.normal(0, noise_std * mag_Z, len(t))
    
    return t, v_signal, i_signal

def extract_impedance_dft(f_stimulus, t, v_signal, i_signal):
    """
    Extract complex impedance Z(f) using a single-bin Discrete Fourier Transform.
    This simulates what the ESP32 would compute from the sampled data.
    """
    N = len(t)
    dt = t[1] - t[0]
    
    # Sine and cosine reference components
    ref_cos = np.cos(2 * np.pi * f_stimulus * t)
    ref_sin = np.sin(2 * np.pi * f_stimulus * t)
    
    # Compute DFT coefficients for Voltage
    V_re = (2.0 / N) * np.sum(v_signal * ref_cos)
    V_im = -(2.0 / N) * np.sum(v_signal * ref_sin)
    V_complex = V_re + 1j * V_im
    
    # Compute DFT coefficients for Current
    I_re = (2.0 / N) * np.sum(i_signal * ref_cos)
    I_im = -(2.0 / N) * np.sum(i_signal * ref_sin)
    I_complex = I_re + 1j * I_im
    
    # Complex Impedance Z = V / I
    if np.abs(I_complex) < 1e-9:
        return np.nan + 1j*np.nan
        
    Z = V_complex / I_complex
    return Z

def sweep_frequencies(frequencies, true_Z_array, sampling_rate=860, duration=1.0):
    """
    Run the software recreation of the hardware pipeline over a suite of frequencies.
    """
    Z_estimated = []
    
    for f, Z_actual in zip(frequencies, true_Z_array):
        # The true 860 SPS might alias if f > 430 Hz, let's observe this!
        t, v, i = generate_signals(f, Z_actual, sampling_rate, duration)
        Z_est = extract_impedance_dft(f, t, v, i)
        Z_estimated.append(Z_est)
        
    return np.array(Z_estimated)

if __name__ == "__main__":
    print("DFT Impedance Extraction Script available.")
