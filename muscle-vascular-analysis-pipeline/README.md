# Astrocyte–Vascular Analysis Pipeline (MATLAB)

> **Repo:** `BIONIC-Lab/astrocyte-vascular-analysis-pipeline`  
> **Author:** Ashvin Handoo  
> **Last Updated:** 2025-10-26

A MATLAB-based pipeline demonstrating **quantitative analysis of vasomotion and smooth-muscle calcium dynamics**, with a focus on **transfer entropy (TE)** using **Kraskov** and **kernel** estimators. This project is designed as a **recruiter-friendly portfolio** for bioinformatics / biocomputation roles, emphasizing signal processing, statistical modeling, and reproducible workflows.

This repository includes a **synthetic dataset generator** so reviewers can run the demo without access to lab data.

---

## 🧩 Project Structure

```
astrocyte-vascular-analysis-pipeline/
├── src/
│   ├── analysis/                # TE estimators & meta-analysis
│   ├── visualization/           # Plotting utilities
│   ├── core/                    # Orchestration wrappers
│   ├── utils/                   # Synthetic data generation
│   └── runDemoPipeline.m        # End-to-end runnable demo
├── results/
│   ├── synthetic_data/          # Auto-generated demo data
│   └── generated_plots/         # Figures created by the demo
├── docs/                        # Notes/diagrams if needed
├── REQUIREMENTS.md              # MATLAB version/toolboxes
├── .gitignore
└── LICENSE
```

---

## 🚀 Quick Start (Demo Mode)

In MATLAB:
```matlab
% From the repo root:
addpath(genpath('src'));
runDemoPipeline
% Outputs:
% - results/vascular_output_summary.csv
% - results/generated_plots/synthetic_vascular_corr.png
```

> The demo computes a **rolling correlation** between synthetic vasomotion and calcium signals as an intuitive coupling proxy. TE scripts are preserved with their original logic and can be applied to the same synthetic data or to lab datasets if available to you.

---

## 🔧 Skills Demonstrated

- **MATLAB for physiological signals**
- **Transfer Entropy (Kraskov & kernel estimators)**
- **Time-series analysis:** lag, cross-correlation, rolling metrics
- **Reproducibility:** synthetic data generator with deterministic seeds
- **Communication:** professional documentation and modular structure

---

## 🧪 Data Availability

Original experiment data are not included. This repo ships with a **synthetic generator** (`src/utils/generateSyntheticVascularData.m`) to enable full reproducibility for reviewers.

---

## 📦 Selected Modules

- `src/analysis/transferEntropyKraskov.m` — Kraskov TE estimator (renamed from original JIDT script).
- `src/analysis/transferEntropyKernel.m` — Kernel-based TE calculation.
- `src/analysis/metaAnalysisPipeline.m` — Batch-level meta-analysis.
- `src/analysis/metaAnalysisSingle.m` — Single-dataset meta-analysis.
- `src/visualization/plotVascularCorrelation.m` — Plot coupling and outcomes.
- `src/core/runTransferEntropy.m` — Wrapper/orchestration for TE runs.

Each file includes a header noting its **original filename** for provenance.

---

## 🧰 Requirements

See `REQUIREMENTS.md` for MATLAB version/toolboxes.

---

## 📄 License

MIT License (see `LICENSE`).

---

## 👤 Contact

- **Ashvin Handoo** — Bioengineering | MATLAB | Quantitative Physiology
- GitHub: _link to your profile_
- Email: ash213@pitt.edu
