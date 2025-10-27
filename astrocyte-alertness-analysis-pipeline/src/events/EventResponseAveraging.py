# EventResponseAveraging.py
# -------------------------------------------------------------------------
# Origin: "Dilation event averaging.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   - Computes average pupil and calcium activity across baseline and stimulation events. Produces separate CSVs for each condition.
#
# Inputs:
#   - Event-aligned CSVs (from EventTimeAlignmentPlotting)
#
# Outputs:
#   - 5 CSVs (baseline + stim 1–4) with mean traces
#
# File Relationships:
#   - Used before EventResponseAverageVisualization.
#
# Dependencies:
#   - pandas, numpy, glob, os
# -------------------------------------------------------------------------

import pandas as pd
import glob
import os
import numpy as np

def pad_array(array, max_length):
    """Pads an array with NaN values to match the max_length."""
    pad_length = max_length - array.shape[0]
    if pad_length > 0:
        padding = np.full((pad_length, array.shape[1]), np.nan)
        array = np.vstack([array, padding])
    return array

def average_and_std_rows_from_csvs(files, columns_to_average):
    all_arrays = []
    max_length = 0

    for file in files:
        df = pd.read_csv(file)
        if all(col in df.columns for col in columns_to_average):
            array = df[columns_to_average].to_numpy()
            all_arrays.append(array)
            max_length = max(max_length, array.shape[0])

    # Pad all arrays to have the same length
    padded_arrays = [pad_array(array, max_length) for array in all_arrays]

    # Stack arrays along a new axis and compute the mean and standard deviation along that axis
    stacked_arrays = np.stack(padded_arrays)
    averaged_array = np.nanmean(stacked_arrays, axis=0)
    std_array = np.nanstd(stacked_arrays, axis=0)

    # Create DataFrame from the averaged array
    averaged_df = pd.DataFrame(averaged_array, columns=columns_to_average)

    # Add standard deviation columns to the DataFrame
    for col in columns_to_average:
        averaged_df[f'{col} Std'] = std_array[:, columns_to_average.index(col)]

    return averaged_df

# Define input and output directories
input_directory = r"C:\Users\ASH213\Documents\Correlated\890\dilation+constriction_events"
output_directory = r"C:\Users\ASH213\Documents\Correlated\890"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Get list of all CSV files in the input directory
all_csv_files = glob.glob(os.path.join(input_directory, "*.csv"))

# Separate files into baseline and stim groups
baseline_files = [file for file in all_csv_files if "baseline" in file or "stimcondition_5" in file]
stimcondition_1_files = [file for file in all_csv_files if "stimcondition_1" in file and "baseline" not in file]
stimcondition_2_files = [file for file in all_csv_files if "stimcondition_2" in file and "baseline" not in file]
stimcondition_3_files = [file for file in all_csv_files if "stimcondition_3" in file and "baseline" not in file]
stimcondition_4_files = [file for file in all_csv_files if "stimcondition_4" in file and "baseline" not in file]

# Print the number of files in each group
print(f"Number of baseline files: {len(baseline_files)}")
print(f"Number of stimcondition_1 files: {len(stimcondition_1_files)}")
print(f"Number of stimcondition_2 files: {len(stimcondition_2_files)}")
print(f"Number of stimcondition_3 files: {len(stimcondition_3_files)}")
print(f"Number of stimcondition_4 files: {len(stimcondition_4_files)}")

# Define columns to be used
columns_to_average = ["Pupil Diameter Ratio", "calcium"]

# Compute averages and standard deviations for baseline files
baseline_averages = average_and_std_rows_from_csvs(baseline_files, columns_to_average)
baseline_averages.to_csv(os.path.join(output_directory, "baseline_averaged_results.csv"), index=False)

# Compute averages and standard deviations for each stimulation condition
stim_conditions = {
    "stimcondition_1": stimcondition_1_files,
    "stimcondition_2": stimcondition_2_files,
    "stimcondition_3": stimcondition_3_files,
    "stimcondition_4": stimcondition_4_files,
}

for condition, files in stim_conditions.items():
    stim_averages = average_and_std_rows_from_csvs(files, columns_to_average)
    stim_averages.to_csv(os.path.join(output_directory, f"{condition}_averaged_results.csv"), index=False)

print("Averaged values and standard deviations saved to 'baseline_averaged_results.csv' and respective stimulation condition files")
