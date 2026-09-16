# Algorithm & Mathematical Pipeline

## Discrete Fourier Transform (DFT) for Impedance Extraction

Commercial potentiostats rely on lock-in amplifiers to extract exact phase and magnitude. To achieve this on a cheap ESP32, we use a single-bin Discrete Fourier Transform (DFT).

For an injected stimulus frequency $f_{stim}$:

1. Read voltage $v(t)$ and current $i(t)$ arrays simultaneously from the ADS1115.
2. Generate local reference sine and cosine waves at $f_{stim}$.
3. Multiply and integrate to find the real and imaginary components of $V$ and $I$.

$$ V_{complex} = \frac{2}{N} \sum v(t)\cos(\omega t) - j \frac{2}{N} \sum v(t)\sin(\omega t) $$
$$ Z(f_{stim}) = \frac{V_{complex}}{I_{complex}} $$

## Equivalent Circuit Model (Randles)

We map the impedance spectra roughly to a simplified **Randles Circuit**:

- **R0**: Series ohmic resistance (estimated via high frequency real-intercept).
- **Rct**: Charge transfer resistance (width of the semicircular arc).
- **Cdl**: Double-layer capacitance.
- **Zdiff**: Warburg tail showing low frequency diffusion.

Instead of heavy Complex Non-linear Least Squares (CNLS) fitting on the ESP32, the pipeline extracts heuristic features:

- `Z_mag_1Hz`
- `Phase_10Hz`
- `R_ohm_est` (High frequency real estimate)
- `R_pol_est` (Low freq minus High freq real span)
- `Max_Img_Z` (Capacitive peak)

## Machine Learning

These extracted heuristic features are fed into a **Random Forest Regressor** trained against capacity-based State-of-Health labels (via the NASA dataset). This turns the inexpensive hardware readings into an actionable battery condition inference.
