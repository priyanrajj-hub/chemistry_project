import numpy as np

def extract_features(frequencies, Z_array):
    """
    Extract basic features from the complex impedance spectrum.
    Since this is a low-cost demonstrator, we don't perform full non-linear 
    least squares fitting (CNLS) for Randles circuit on the ESP32.
    Instead, we extract robust heuristic features.
    
    Features:
    - R_ohm (High Frequency Intercept ~ R0)
    - R_pol (Low Frequency Intercept minus High Frequency Intercept ~ Rct)
    - Z_mag_1Hz (Magnitude of impedance at low frequency)
    - Phase_10Hz (Phase angle at mid frequency)
    - Max_Img_Z (Maximum imaginary value, representing the top of the semicircle)
    """
    Z_re = np.real(Z_array)
    Z_im = np.imag(Z_array)
    Z_mag = np.abs(Z_array)
    Z_phase = np.angle(Z_array, deg=True)
    
    # High frequency is at the end of the array if frequencies are descending, 
    # but let's just find the max/min frequencies mathematically.
    idx_hf = np.argmax(frequencies)
    idx_lf = np.argmin(frequencies)
    
    # High-frequency x-axis intercept approximation (R0)
    # R0 is approx the real resistance when imaginary part is closest to 0 at high freq
    R_ohm = Z_re[idx_hf] 
    
    # Polarization resistance approximation
    # Estimated as the span of the semi-circle on the real axis
    # Here we roughly take LF real part minus HF real part
    R_lf = Z_re[idx_lf]
    R_pol = max(0, R_lf - R_ohm)
    
    # Max peak of the arc (imaginary part)
    # Note: imaginary part is usually negative in standard Nyquist, so we take min() and negate
    Max_Img_Z = np.abs(np.min(Z_im))
    
    # Some specific single-frequency features often used in cheap embedded ML
    # Find closest index to 1Hz
    idx_1hz = (np.abs(frequencies - 1.0)).argmin()
    Z_mag_1Hz = Z_mag[idx_1hz]
    
    # Find closest index to 10Hz
    idx_10hz = (np.abs(frequencies - 10.0)).argmin()
    Phase_10Hz = Z_phase[idx_10hz]
    
    return {
        'R_ohm_est': R_ohm,
        'R_pol_est': R_pol,
        'Max_Img_Z': Max_Img_Z,
        'Z_mag_1Hz': Z_mag_1Hz,
        'Phase_10Hz': Phase_10Hz
    }
