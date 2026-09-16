# Project Overview

## The Problem

Lithium-ion batteries powers our modern world—from smartphones to electric vehicles. However, they degrade both electrically and chemically in ways that are completely invisible to standard voltage checks or coulomb counting. Electrochemical Impedance Spectroscopy (EIS) can reveal internal state changes, such as charge-transfer resistance growth and internal short-circuit (ISC) risks. Unfortunately, commercial EIS potentiostats cost upwards of \$5,000 to \$15,000, making them completely inaccessible for undergraduate research, educational contexts, and low-resource environments.

## The Approach

This project bridges the gap by demonstrating an extreme low-cost (~₹2,500 / ~$30) implementation of an EIS measurement rig. Utilizing an ESP32 microcontroller, an AD9833 programmable waveform generator, and an ADS1115 16-bit ADC, the hardware applies a controllable AC excitation signal and measures the voltage and current response at low frequencies (due to an 860 SPS sampling limit).

By extracting complex impedance features (roughly mapping to a Randles circuit: R0, Rct, Cdl, Zdiff), we apply Machine Learning (Random Forest regression) to predict the State of Health (SoH). We validate the data pipelines on the public NASA Li-ion Battery Aging Dataset, proving that proxy features are just as predictive in accessible setups as they are in high-end commercial rigs.

## Novelty and Contribution

**This project does not invent new electrochemistry.** The scientific literature showing ML + EIS correlates to battery aging is already well-established.

The true novelty lies in **engineering accessibility, transparency, safety, and sustainability.** We bring advanced diagnostic techniques out of the multi-million dollar laboratory and give them to students, hackers, and makers.
