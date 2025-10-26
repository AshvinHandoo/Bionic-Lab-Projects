# Astrocyte Alertness Analysis Pipeline

> **Repo:** `BIONIC-Lab/astrocyte-alertness-analysis-pipeline`  
> **Author:** Ashvin Handoo  
> **Last Updated:** 2025-10-26

A Python-based analysis pipeline demonstrating a **bioinformatics / computational neuroscience** workflow:
- Signal processing for time-series data (pupil diameter ratio, calcium traces)
- Correlation analysis and event-detection patterns
- Modular, well-documented code suited for **R&D data science** roles

This repository uses a small **synthetic dataset** (generated on-the-fly) so reviewers can run the code without access to the original lab data.

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
│   ├── utils/              # Synthetic data generator and shared helpers
│   └── run_demo_pipeline.py
├── results/
│   ├── synthetic_data/     # Auto-generated demonstration CSVs
│   └── generated_plots/    # Auto-generated figures
├── docs/                   # Diagrams/notes if needed
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## 🚀 Quick Start (Demo Mode)

```bash
# 1) Create environment (example)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run the synthetic demo
python -m src.run_demo_pipeline

# Outputs:
# - results/output_summary.csv
# - results/generated_plots/synthetic_signals_and_corr.png
```
The demo computes a **rolling correlation** between synthetic pupil and calcium signals to illustrate an **alertness proxy**.

> Note: Original experimental data are unavailable; this repo is intentionally **portfolio-focused** for computational/bioinformatics roles.

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

The original lab datasets are not included. For demonstration:
- We generate a small synthetic dataset under `results/synthetic_data/astrocyte_signals.csv`.
- Scripts designed for the original data should be considered **archival logic** and may require path tweaks to run end-to-end; they’re preserved for **technical depth**.

---

## 📄 License

This repository is released under the MIT License (see `LICENSE`).

---

## 👤 Contact

- **Ashvin Handoo** — Bioengineering | Python | Data Analysis
- GitHub: https://github.com/AshvinHandoo
- Email: ash213@pitt.edu
