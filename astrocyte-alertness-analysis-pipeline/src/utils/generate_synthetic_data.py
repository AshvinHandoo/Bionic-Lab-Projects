"""
Generate small synthetic pupil and calcium datasets for demonstration.

Outputs:
    results/synthetic_data/astrocyte_signals.csv
        Columns: time, pupil_diameter_ratio, calcium

The signals are composed of sinusoids + noise with segments of higher
correlation to mimic varying alertness states.
"""
import os
import numpy as np
import pandas as pd

def generate(seed: int = 42, n: int = 3000, fs: float = 10.0, out_dir: str = None):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / fs

    # Base signals
    calcium = 0.6*np.sin(2*np.pi*0.2*t) + 0.3*np.sin(2*np.pi*0.05*t + 1.0) + 0.1*rng.standard_normal(n)
    pupil = 0.4*np.sin(2*np.pi*0.2*t + 0.3) + 0.2*np.sin(2*np.pi*0.05*t - 0.5) + 0.15*rng.standard_normal(n)

    # Inject "alert" segments with higher coupling
    for start in [500, 1400, 2200]:
        end = start + 250
        if end > n: end = n
        pupil[start:end] = 0.6*calcium[start:end] + 0.2*rng.standard_normal(end-start)

    df = pd.DataFrame({
        "time": t,
        "Pupil Diameter Ratio": pupil,
        "calcium": calcium
    })

    out_dir = out_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "results", "synthetic_data")
    os.makedirs(out_dir, exist_ok=True)
    out_csv = os.path.join(out_dir, "astrocyte_signals.csv")
    df.to_csv(out_csv, index=False)
    return out_csv

if __name__ == "__main__":
    path = generate()
    print(f"Synthetic data written to: {path}")
