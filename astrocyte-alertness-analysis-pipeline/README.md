# Astrocyte Alertness Analysis Pipeline

> **Repo:** `BIONIC-Lab/astrocyte-alertness-analysis-pipeline`  
> **Author:** Ashvin Handoo  
> **Last Updated:** 2025-10-26

A Python-based analysis pipeline demonstrating a **computational neuroscience** workflow:
- Signal processing for time-series data (pupil diameter ratio, calcium traces)
- Correlation analysis and event-detection patterns
- Modular, well-documented code meant for **data science** roles

---

## 🧩 Project Structure

```
astrocyte-alertness-analysis-pipeline/
├── src/
│   ├── io/                 # Data I/O and serialization helpers
│   ├── preprocessing/      # Cleaning, thresholding, interpolation, video preprocess
│   ├── analysis/           # Cross-corr, lag, distributions
│   ├── events/             # Event detection, averaging, plotting
│   ├── visualization/      # Plotting utilities, video players
├── requirements.txt
├── .gitignore
└── LICENSE
```
---

## 🔧 Notable Skills Demonstrated

- **Python data science stack:** `pandas`, `numpy`, `matplotlib`
- **Signal processing:** rolling correlation, derivatives, thresholding
- **Modular code design:** functional separation (I/O, preprocessing, analysis, viz)
- **Reproducibility:** synthetic data + deterministic seeds
- **Documentation:** docstrings, READMEs, and clear folder conventions

---

## 📦 Modules (Selected)

- `src/analysis/cross_correlation.py` — cross-correlation utilities (from original lab scripts).
- `src/analysis/dilation_lag_analysis.py` — lag analysis around dilation events.
- `src/events/dilation_event_averaging.py` — event alignment and averaging.
- `src/preprocessing/pupil_derivative_thresholding.py` — derivative-based event detection.
- `src/visualization/derivative_graphing.py` — derivative and trace plotting helpers.
- `src/utils/generate_synthetic_data.py` — deterministic demo data generation.

Each file includes a header with the original filename for provenance.

---

## 🧪 Data Availability

The original lab datasets are not included.

---

## 📄 License

This repository is released under the MIT License (see `LICENSE`).

---

## 👤 Contact

- **Ashvin Handoo** — Bioengineering | Data Analysis
- GitHub: https://github.com/AshvinHandoo
- Email: ash213@pitt.edu
