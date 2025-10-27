# EventTimeAlignmentPlotting.py
# -------------------------------------------------------------------------
# Origin: "Dilation event plotting.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   Plots individual dilation events aligned in time, distinguishing baseline
and stimulation conditions, and outputs event-aligned CSVs.
#
# Inputs:
#   - Event CSVs ('bindist_2020' or 'bindist_2040')
#
# Outputs:
#   - Plots and aligned CSVs for each event
#
# File Relationships:
#   - Precedes EventResponseAveraging.
#
# Dependencies:
#   pandas, numpy, matplotlib
# -------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the main directory
main_directory = r"C:\Users\ASH213\Documents\Correlated\890"

# Define days, trials, and stimulation conditions
days = ['d084', 'd070', 'd056', 'd028', 'd021', 'd014', 'd007', 'd003', 'd001']
trials = ['trial_1', 'trial_2', 'trial_3']
stim_conditions = ['stimcondition_1', 'stimcondition_2', 'stimcondition_3', 'stimcondition_4', 'stimcondition_5']

# Create a directory for saving plots and results
output_directory = os.path.join(main_directory, "dilation+constriction_events")
os.makedirs(output_directory, exist_ok=True)

# DataFrame to store time differences
time_differences = pd.DataFrame(columns=['Day', 'Trial', 'StimCondition', 'Index', 'TimeDifference'])

# Process each day, trial, and stimulation condition
for day in days:
    for trial in trials:
        for stim_condition in stim_conditions:
            # Construct the file path
            file_path = os.path.join(main_directory, day, trial, stim_condition, 'bindist_2040.csv')

            # Check if the file exists
            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                continue

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Find indices where 'yes' appears in the 'threshold' column
            yes_indices = []
            last_idx = -100  # Initialize last index to a large number

            for idx, row in df.iterrows():
                if row['threshold'] == 'yes' and idx - last_idx > 50:
                    yes_indices.append(idx)
                    last_idx = idx

            # Categorize indices
            baseline_indices = []
            stim_indices = []

            for idx in yes_indices:
                if idx < 299:
                    baseline_indices.append(idx)
                elif 299 < idx < 598:
                    stim_indices.append(idx)
                else:
                    baseline_indices.append(idx)

            # Process indices with "stim" category first
            for idx in stim_indices + baseline_indices:
                subset_type = ""
                if idx < 299:
                    start_idx = max(idx - 50, 0)
                    end_idx = min(idx + 150, len(df))
                    subset = df.iloc[start_idx:end_idx]
                    subset_type = "baseline"
                elif 299 < idx < 598:
                    start_idx = max(idx - 50, 0)
                    end_idx = min(idx + 150, len(df))
                    subset = df.iloc[start_idx:end_idx]
                    subset_type = "stim"
                elif idx > 598:
                    start_idx = max(idx - 50, 0)
                    end_idx = min(idx + 150, len(df))
                    subset = df.iloc[start_idx:end_idx]
                    subset_type = "baseline"

                # Store the original subset for plotting
                original_subset = subset.copy()

                # Pad the subset with NaNs if necessary to make it 200 rows long
                if len(subset) < 200:
                    if start_idx == 0:
                        padding_needed = 200 - len(subset)
                        padding = pd.DataFrame(np.nan, index=range(padding_needed), columns=subset.columns)
                        subset = pd.concat([padding, subset]).reset_index(drop=True)
                    elif end_idx == len(df):
                        padding_needed = 200 - len(subset)
                        padding = pd.DataFrame(np.nan, index=range(padding_needed), columns=subset.columns)
                        subset = pd.concat([subset, padding]).reset_index(drop=True)
                    else:
                        padding_needed = 200 - len(subset)
                        start_padding = pd.DataFrame(np.nan, index=range(padding_needed // 2), columns=subset.columns)
                        end_padding = pd.DataFrame(np.nan, index=range(padding_needed - padding_needed // 2),
                                                   columns=subset.columns)
                        subset = pd.concat([start_padding, subset, end_padding]).reset_index(drop=True)

                # Calculate time difference between max calcium and max pupil diameter ratio
                max_calcium_time = subset['time'][subset['calcium'].idxmax()]
                max_pupil_time = subset['time'][subset['Pupil Diameter Ratio'].idxmax()]
                time_difference = (max_calcium_time - max_pupil_time)

                # Adjust subset size if time_difference exceeds 5
                while abs(time_difference) > 5 and len(subset) > 50:  # Ensure subset doesn't become too small
                    subset_length = len(subset) // 2
                    center_idx = (start_idx + end_idx) // 2
                    start_idx = max(center_idx - subset_length // 2, 0)
                    end_idx = min(center_idx + subset_length // 2, len(df))
                    subset = df.iloc[start_idx:end_idx].reset_index(drop=True)

                    # Recalculate time difference with new subset
                    max_calcium_time = subset['time'][subset['calcium'].idxmax()]
                    max_pupil_time = subset['time'][subset['Pupil Diameter Ratio'].idxmax()]
                    time_difference = (max_calcium_time - max_pupil_time)

                # Append the result to the DataFrame using concat
                time_differences = pd.concat([time_differences, pd.DataFrame({
                    'Day': [day],
                    'Trial': [trial],
                    'StimCondition': [stim_condition],
                    'Index': [idx],
                    'TimeDifference': [time_difference]
                })], ignore_index=True)

                # Generate and save plots for each subset using the original subset
                # Create figure and axis objects
                fig, ax1 = plt.subplots()

                # Plot Calcium on primary y-axis (ax1)
                ax1.plot(original_subset['time'], original_subset['calcium'], label='Calcium', color='blue')
                ax1.set_xlabel('Time')
                ax1.set_ylabel('Calcium', color='blue')
                ax1.tick_params(axis='y', labelcolor='blue')

                # Calculate y-axis limits for Calcium
                max_abs_calcium = original_subset['calcium'].abs().max()
                calcium_ylim = max_abs_calcium  # Adjust for some margin

                ax1.set_ylim(-calcium_ylim, calcium_ylim)

                # Create secondary y-axis for Pupil Diameter Ratio
                ax2 = ax1.twinx()
                ax2.plot(original_subset['time'], original_subset['Pupil Diameter Ratio'], label='Pupil Diameter Ratio', color='green')
                ax2.set_ylabel('Pupil Diameter Ratio', color='green')
                ax2.tick_params(axis='y', labelcolor='green')

                # Set y-axis limits for Pupil Diameter Ratio (0 to 1)
                max_abs_pupil = original_subset['Pupil Diameter Ratio'].abs().max()
                ax2.set_ylim(0, max_abs_pupil)

                # Mark the max calcium and max pupil times
                ax1.axvline(x=max_calcium_time, color='red', linestyle='--', label='Max Calcium Time')
                ax2.axvline(x=max_pupil_time, color='purple', linestyle='--', label='Max Pupil Time')

                # Set title and save plot
                plt.title(f'Plot around index {idx} for {day} - {trial} - {stim_condition}')
                plt.tight_layout()

                # Add legends
                fig.legend(loc='upper right', bbox_to_anchor=(0.85, 0.85))

                # Save the plot
                plot_filename = f"{day}_{trial}_{stim_condition}_index_{idx}.png"
                plot_filepath = os.path.join(output_directory, plot_filename)
                plt.savefig(plot_filepath)
                plt.close(fig)

                # Save the subset to a CSV file
                if not subset.empty:
                    subset_filename = f"{day}_{trial}_{stim_condition}_{subset_type}_index_{idx}.csv"
                    subset_filepath = os.path.join(output_directory, subset_filename)
                    subset.to_csv(subset_filepath, index=False)

            print(f"Processed {day} - {trial} - {stim_condition}")

# Save time differences to CSV
time_differences.to_csv(os.path.join(output_directory, 'time_differences.csv'), index=False)
