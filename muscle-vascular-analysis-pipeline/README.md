# Muscle–Vascular Analysis Pipeline (MATLAB)

> **Repo:** `BIONIC-Lab/muscle-vascular-analysis-pipeline`  
> **Author:** Ashvin Handoo  
> **Last Updated:** 2025-10-26

A MATLAB-based pipeline demonstrating **quantitative analysis of vasomotion and smooth-muscle calcium dynamics**, with a focus on **transfer entropy (TE)** using **Kraskov** and **kernel** estimators. This project is designed as a **recruiter-friendly portfolio** for bioinformatics / biocomputation roles, emphasizing signal processing, statistical modeling, and reproducible workflows.

---

## 🧩 Project Structure

```
muscle-vascular-analysis-pipeline/
├── src/
│   ├── analysis/                # TE estimators & meta-analysis
│   ├── visualization/           # Plotting utilities
│   ├── utils/                   # Synthetic data generation
├── REQUIREMENTS.md              # MATLAB version/toolboxes
├── .gitignore
└── LICENSE
```
---

## 🔧 Skills Demonstrated
- **MATLAB for quantitative physiology:** designed scripts to analyze smooth muscle calcium and vasomotion activity.
- **Transfer entropy analysis:** implemented Kraskov and kernel estimators using (JIDT) to quantify directional coupling between signals.
- **Time-series modeling:** evaluated lag structure, correlation strength, and coupling stability across multiple vessels and conditions.
- **Statistical visualization:** generated comparative plots of forward vs. reverse signal influence and varying lag to explore signal relationship

---

## 🧪 Data Availability

Original experiment data are not included.

---

## 📦 Selected Modules

- `src/analysis/TransferEntropyKraskov.m` — Kraskov TE estimator (renamed from original JIDT script).
- `src/analysis/TransferEntropyKernel.m` — Kernel-based TE calculation.
- `src/analysis/MetaAnalysisMulti.m` — Multi-animal meta-analysis.
- `src/analysis/MetaAnalysisSingle.m` — Single-animal meta-analysis.
- `src/visualization/PlotVascularCorrelation.m` — Complete Plot coupling and outcomes.

Each file includes a header noting its **original filename** for provenance.

---

## 🧰 Requirements

See `REQUIREMENTS.md` for MATLAB version/toolboxes.

---

## 📄 License

MIT License (see `LICENSE`).

---

## 👤 Contact

- **Ashvin Handoo** — Bioengineering | MATLAB
- GitHub: https://github.com/AshvinHandoo
- Email: ash213@pitt.edu
