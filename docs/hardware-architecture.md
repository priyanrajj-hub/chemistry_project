# Hardware Architecture

The overarching goal was to maintain an ultra-low budget (under ₹2,500) while obtaining usable excitation signals and digitizing the response.

## Block Diagram

```
[ESP32] (I2C/SPI control)
   ├──> [AD9833] (Generates precise sine wave)
   │       └──> [Power Amplifier/Op-Amp] (Current buffer)
   │               └──> [Li-Ion Cell Under Test]
   │                       └──> [Shunt Resistor]
   └──> [ADS1115] (Reads V_cell and V_shunt at max 860 SPS)
             └──> [ESP32] (Computes Phase & Magnitude via single-bin DFT)
```

## Bill of Materials (Budget Estimate)

*Note: All cost numbers are estimates for budget planning, not official vendor quotes.*

| Component | Purpose | Estimated Cost (INR) |
| --- | --- | --- |
| ESP32 Dev Board | System controller & Wi-Fi logging | ₹450 |
| AD9833 Module | Programmable Sine Wave Generator | ₹600 |
| ADS1115 Module | 16-bit ADC (I2C) | ₹350 |
| LM358 / OpAmps | Signal buffering and amplification | ₹100 |
| Precision Shunt | Current measurement | ₹150 |
| Proxy RC comps. | Resistors/Capacitors for Safe Testing | ₹100 |
| Breadboard/Wires | Prototyping | ₹350 |
| Misc. Components | Connectors, headers, protective diodes | ₹340 |
| **Total** | | **~₹2,440** ($\approx \$30$) |

## Feasibility and Constraints

The main bottleneck in this budget rig is the **ADS1115 ADC**. While it boasts 16-bit resolution, its maximum sampling rate is 860 SPS (Samples Per Second). According to the Nyquist theorem, this dictates that the absolute maximum frequency we can inject and analyze is ~430 Hz, though realistically we limit excitation to $< 100$ Hz to ensure sufficient points per period for DFT accuracy.

This makes it a **Low-Frequency Demonstrator**, suitable only for observing overarching phenomena like charge-transfer resistance (Rct) and diffusion (Warburg impedance), rather than highly detailed high-frequency ohmic responses.
