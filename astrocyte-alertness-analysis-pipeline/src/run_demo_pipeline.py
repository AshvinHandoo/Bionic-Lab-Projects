"""
Demo runner for astrocyte-alertness-analysis-pipeline using synthetic data.

This script:
  1) Generates synthetic time-series (pupil + calcium)
  2) Computes a rolling correlation (as a simple alertness proxy)
  3) Saves a summary CSV and a plot into results/

Usage:
  python -m src.run_demo_pipeline
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.utils.generate_synthetic_data import generate

ROOT = os.path.dirname(os.path.dirname(__file__))
RES_DIR = os.path.join(ROOT, "results")
PLOT_DIR = os.path.join(RES_DIR, "generated_plots")

os.makedirs(PLOT_DIR, exist_ok=True)

# 1) Generate synthetic data
csv_path = generate()
df = pd.read_csv(csv_path)

# 2) Rolling correlation between pupil and calcium (simple proxy)
window = 101  # ~10s at 10 Hz
corr = df["Pupil Diameter Ratio"].rolling(window, center=True).corr(df["calcium"])
df["rolling_corr"] = corr

# 3) Save summary
out_csv = os.path.join(RES_DIR, "output_summary.csv")
df.to_csv(out_csv, index=False)

# 4) Plot
fig = plt.figure(figsize=(10, 5))
ax1 = plt.gca()
ax1.plot(df["time"], df["Pupil Diameter Ratio"], label="Pupil")
ax1.plot(df["time"], df["calcium"], label="Calcium", alpha=0.8)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Signal")
ax1.legend(loc="upper right")

ax2 = ax1.twinx()
ax2.plot(df["time"], df["rolling_corr"], label="Rolling Corr", alpha=0.6)
ax2.set_ylabel("Rolling Corr")

plt.title("Synthetic Pupil & Calcium Signals with Rolling Correlation")
out_png = os.path.join(PLOT_DIR, "synthetic_signals_and_corr.png")
plt.tight_layout()
plt.savefig(out_png, dpi=150)
plt.close(fig)

print(f"Summary saved to: {out_csv}")
print(f"Plot saved to: {out_png}")
