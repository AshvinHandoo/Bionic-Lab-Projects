# Astrocyte Alertness Analysis Pipeline (Python)

> **Repo:** `BIONIC-Lab/astrocyte-alertness-analysis-pipeline`  
> **Author:** Ashvin Handoo  
> **Last Updated:** 2025-10-26

A Python-based analysis pipeline for **astrocyte calcium activity** and **pupil diameter dynamics**, exploring their relationship under varying alertness states.  
This repository demonstrates skills in **signal processing**, **event analysis**, and **computational neuroscience** workflows, built as a **recruiter-facing portfolio** project.

---

## 🧩 Project Structure

```
astrocyte-alertness-analysis-pipeline/
├── src/
│   ├── preprocessing/      # Calcium & pupil preprocessing, video handling
│   ├── analysis/           # Correlation, lag, and coupling analysis
│   ├── events/             # Dilation event detection, averaging, visualization
│   ├── visualization/      # Plotting & dual video playback
│   └── utils/              # Helper conversions and thresholding
├── REQUIREMENTS.md
├── .gitignore
└── LICENSE
```

---

## 🔧 Skills Demonstrated
- **Python Data Science Stack:** `pandas`, `numpy`, `matplotlib`, `scipy`
- **Signal Analysis:** correlation, lag estimation, event detection
- **Computational Neuroscience:** analysis of pupil–calcium coupling as an alertness metric
- **Scientific Visualization:** time-series plotting and event-based animation
- **Software Organization:** modular structure and function-level documentation

---

## 📦 Selected Modules

- `src/analysis/CalciumPupilCouplingAnalysisNormalized.py` — coupling between normalized calcium and pupil signals  
- `src/events/DilationEventDetection.py` — identifies significant pupil dilation events  
- `src/events/EventResponseAveraging.py` — averages responses across events  
- `src/visualization/RawSignalVisualization.py` — raw calcium & pupil plotting  
- `src/preprocessing/DeepLabCutInterpolation.py` — interpolates DeepLabCut probability data  

---

## 🧰 Requirements
See `REQUIREMENTS.md` for Python version and dependencies.

---

## 📄 License
MIT License (see `LICENSE`).

---

## 👤 Contact
- **Ashvin Handoo** — Bioengineering | Data Analysis  
- GitHub: https://github.com/AshvinHandoo  
- Email: ash213@pitt.edu
