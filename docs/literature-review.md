# Literature Review

The following key literature forms the scientific basis for our approach. *Note: We do not claim to match the published high-end accuracies (e.g. RMSE < 3%), but use them as the theoretical benchmark validating the methodology.*

1. **Severson et al., Nature Communications (2020)** — Demonstrates early prediction of battery cycle life using EIS and Gaussian-process Machine Learning. Validates ML applied directly to impedance trends.
2. **Li et al., Journal of Energy Storage (2020)** — Explores Equivalent Circuit Modeling (ECM) combined with Artificial Neural Networks (ANN) for SoH estimation, which inspired our heuristic feature-extraction approach.
3. **Schindler et al., Journal of Power Sources (2021)** — A critical review identifying exact EIS signatures indicating aging mechanisms like SEI layer thickening and loss of lithium inventory.
4. **Review, Protection and Control of Modern Power Systems (2023)** — Comprehensive review highlighting how structural AI integration with EIS data is becoming a dominant paradigm for remaining useful life predictions.
5. **Wang et al., Electrochimica Acta (2025)** — Proposes using Convolutional Autoencoders and Random Forests for very early Internal Short Circuit (ISC) detection via EIS sweeps, pointing out critical frequency anomalies.
6. **Journal of Energy Storage (2026)** — Evaluates XGBoost/RF stacking mechanisms utilizing highly compact and summarized EIS features instead of the entire spectrum to drastically reduce inference time.
7. **Journal of Energy Storage (2026)** — Introduces CNN-LSSVM on narrowed characteristic frequency subsets, proving that an entire broadband spectrum $>1kHz$ is not always necessary for health evaluation.
8. **Systematic review, Journal of Energy Engineering (2026)** — Synthesizes the last decade of data-driven battery management, pointing towards cost and hardware accessibility as the final barrier to wide-scale adoption.

**Data & Hardware Components:**
9.  **NASA PCoE** — The Li-ion Battery Aging Dataset utilized to benchmark capacity degradation baselines.
10. **Analog Devices** — AD9833 Datasheet, validating low power programmable waveform generation.
11. **Texas Instruments** — ADS1115 Datasheet, noting the critical 860 SPS limitation that dictates our low-frequency methodological focus.
