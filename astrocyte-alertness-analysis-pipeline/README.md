# Astrocyte Alertness Analysis Pipeline (Python)

> **Repo:** `BIONIC-Lab/astrocyte-alertness-analysis-pipeline`  
> **Author:** Ashvin Handoo  
> **Last Updated:** 2025-10-26

A Python-based analysis pipeline for astrocyte calcium activity and pupil diameter dynamics, exploring their relationship under varying alertness states. This repository demonstrates skills in signal processing, event analysis, and computational neuroscience workflows.

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
- **Python Data Science Stack:** `pandas`, `numpy`, `matplotlib`
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

## 🧪 Research Context
This analysis pipeline was originally developed for a neuroscience project at the University of Pittsburgh’s BIONIC Lab, where DeepLabCut was used to quantify pupil dynamics from high-speed imaging data. The methods and results were presented through a abstract and poster presentation at the 2024 Biomedical Engineering Society (BMES) Annual Conference. The manuscript for the project is still in preparation.

---

## 👤 Contact
- Ashvin Handoo — Bioengineering | Python  
- GitHub: https://github.com/AshvinHandoo  
- Email: ash213@pitt.edu
