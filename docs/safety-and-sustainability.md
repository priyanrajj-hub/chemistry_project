# Safety and Sustainability

## Safety First

One of the major risks in battery analytics research is the physical destruction or dangerous manipulation of Lithium-Ion cells (e.g., inducing hard short circuits).

**In this project:**

- **Zero destructive testing is performed.**
- We do not deliberately fail or damage live Li-ion cells.
- Internal Short Circuit (ISC) emulation for the Abnormality Detector is performed via **safe, external proxy RC circuits** placed in parallel with the cell. This artificially mimics the drop in low-frequency impedance identical to a dendrite forming, without creating the thermal runaway conditions of a real ISC.

## Sustainability

- **Reusable Modules:** We use standard, easily reprogrammable off-the-shelf development boards rather than single-use PCBs.
- **Minimal Waste:** There are no chemically destroyed batteries. Cells analyzed can be sent to standard authorized battery recycling centers intact.
- **RoHS Compliance:** The selected components (ESP32, AD9833, ADS1115 modules) are widely available in RoHS-compliant forms, minimizing the toxic footprint of the hardware prototype.
