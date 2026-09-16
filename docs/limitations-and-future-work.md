# Limitations & Future Work

## Explicit Constraints

A core goal of this project is academic and engineering honesty. We do not claim to match the broadband accuracy of commercial \$10,000 impedance analyzers.

1. **Hardware Limitation (860 SPS):** The ADS1115 restricts the maximum theoretical Nyquist frequency to 430 Hz, cutting off high-frequency ohmic resistance (R0) details. This is purely a low-frequency demonstrator focused on observable trends.
2. **Benchmark Claims:** The literature benchmarks (e.g., RMSE < 3%, capacity fade models) reflect optimal research environments. Our synthetic validation proves the *viability* of the ML approach, not a claim that the $30 hardware achieves those exact benchmarks in the field yet.
3. **No 4-Wire Kelvin Connections:** The current breadboard prototype uses 2-wire sensing, meaning contact resistances are bundled into the cell impedance reading.

## Future Scope

1. **Faster ADC Upgrades:** Transitioning to an accessible MSPS (Mega Samples per Second) SPI ADC to unlock standard 1kHz - 10kHz battery EIS ranges.
2. **Physics-informed ML (PIML):** Enforcing thermodynamic and physical laws onto the Random Forest or Neural Network to decrease required training size and improve generalization on fresh cells.
3. **On-Microcontroller Inference:** Using tools like TensorFlow Lite for Microcontrollers (TFLM) to deploy the Random Forest model natively on the ESP32, achieving true edge inference without needing an external computer.
4. **4-Wire Sensing Implementation:** Upgrading the hardware harness to eliminate contact resistance artifacts.
