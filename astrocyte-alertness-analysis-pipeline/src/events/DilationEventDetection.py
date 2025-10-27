# DilationEventDetection.py
# -------------------------------------------------------------------------
# Origin: "Dilation events.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   Detects pupil dilation events exceeding a dynamic threshold based on
standard deviation of derivatives. Generates per-condition plots.
#
# Inputs:
#   - Pupil derivative data across trials and stim conditions
#
# Outputs:
#   - Graphs and CSVs of significant dilation events
#
# File Relationships:
#   - Upstream of EventThresholdDetection and EventThresholdDetectionNormalized.
#
# Dependencies:
#   pandas, numpy, matplotlib
# -------------------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Base directory where d084, d070, etc. folders are located
base_dir = r"C:\Users\ASH213\Documents\Correlated\890"

# Subfolders for each day containing trials
days = ['d084', 'd070', 'd014', 'd007', 'd003', 'd001', 'd021', 'd028', 'd056']

# Trials
trials = ['trial_1', 'trial_2', 'trial_3']

# Subfolders for each stim condition
stim_conditions = ['stimcondition_1', 'stimcondition_2', 'stimcondition_3', 'stimcondition_4', 'stimcondition_5']

# Output directory
output_dir = r'C:\Users\ASH213\Documents\Correlated\890'

# The specific file to process
bindist_file = 'bindist_2000.csv'

# Time points for red lines
time_markers = [-0.016464, 30.067352]

# Initialize dictionaries to store aggregated data
agg_derivatives = {stim: [] for stim in stim_conditions}
agg_time_derivatives = {stim: [] for stim in stim_conditions}
agg_calcium_values = {stim: [] for stim in stim_conditions}

# Iterate over each day
for day in days:
    day_dir = os.path.join(base_dir, day)

    # Iterate over each trial
    for trial in trials:
        trial_dir = os.path.join(day_dir, trial)

        # Iterate over each stim condition
        for stim in stim_conditions:
            # Collect all Pupil Diameter Ratio data and compute derivatives
            csv_path = os.path.join(trial_dir, stim, bindist_file)
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                if 'Pupil Diameter Ratio' in df.columns and 'time' in df.columns and 'calcium' in df.columns:
                    pupil_diameter_ratio = df['Pupil Diameter Ratio']
                    time = df['time']
                    calcium = df['calcium']

                    # Compute the derivative of the Pupil Diameter Ratio
                    pupil_derivative = np.gradient(pupil_diameter_ratio, time)

                    # Collect the time and calcium values for the derivatives
                    time_derivatives = time
                    calcium_values = calcium

                    # Aggregate the data
                    agg_derivatives[stim].extend(pupil_derivative)
                    agg_time_derivatives[stim].extend(time_derivatives)
                    agg_calcium_values[stim].extend(calcium_values)
                else:
                    print(f"Missing required columns in {csv_path}")
            else:
                print(f"File not found: {csv_path}")

# Plot aggregated data for each stim condition
for stim in stim_conditions:
    if not agg_derivatives[stim]:
        print(f"No Pupil Diameter Ratio data found for any trial in {stim}")
        continue

    # Use all derivatives
    all_derivatives = np.array(agg_derivatives[stim])
    all_times = np.array(agg_time_derivatives[stim])
    all_calcium_values = np.array(agg_calcium_values[stim])

    # Calculate mean and standard deviation of the derivatives
    mean_derivative = np.mean(all_derivatives)
    std_derivative = np.std(all_derivatives)

    # Filter derivatives that are 4 standard deviations away from the mean
    threshold = 2 * std_derivative
    indices = np.where(np.abs(all_derivatives - mean_derivative) >= threshold)[0]
    filtered_derivatives = all_derivatives[indices] if len(indices) > 0 else np.array([])
    filtered_times = all_times[indices] if len(indices) > 0 else np.array([])
    filtered_calcium_values = all_calcium_values[indices] if len(indices) > 0 else np.array([])

    # Debugging outputs
    print(f"Stim Condition: {stim}")
    print(f"Total Derivatives: {len(all_derivatives)}")
    print(f"Filtered Derivatives: {len(filtered_derivatives)}")

    # Find the lowest positive and largest negative derivatives that exceed the threshold
    positive_derivatives = filtered_derivatives[filtered_derivatives > 0]
    negative_derivatives = filtered_derivatives[filtered_derivatives < 0]

    if len(positive_derivatives) > 0:
        lowest_positive_derivative = np.min(positive_derivatives)
    else:
        lowest_positive_derivative = None

    if len(negative_derivatives) > 0:
        largest_negative_derivative = np.max(negative_derivatives)
    else:
        largest_negative_derivative = None

    # Create plots
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle(f'Derivative Analysis for {stim} - {bindist_file}', fontsize=16)

    # Plot the distribution of all derivative values of Pupil Diameter Ratio
    axs[0].hist(all_derivatives, bins=30, color='g', alpha=0.7)
    axs[0].set_title('Distribution of All Pupil Diameter Ratio Derivatives')
    axs[0].set_xlabel('Pupil Diameter Ratio Derivative')
    axs[0].set_ylabel('Frequency')

    # Check if there are any filtered derivatives to plot
    if len(filtered_derivatives) > 0:
        # Plot the time and calcium value for each filtered derivative
        sc = axs[1].scatter(filtered_times, filtered_calcium_values, c=filtered_derivatives, cmap='viridis', alpha=0.7)
        axs[1].set_title('Derivatives 2 Std Dev Away from Mean with Time and Calcium Values')
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Calcium Value')
        cbar = plt.colorbar(sc, ax=axs[1])
        cbar.set_label('Pupil Diameter Ratio Derivative')
    else:
        axs[1].text(0.5, 0.5, 'No derivatives exceed the threshold', horizontalalignment='center',
                    verticalalignment='center')
        axs[1].set_title('No Derivatives 4 Std Dev Away from Mean')
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Calcium Value')

    # Add red vertical lines at specified time points
    for time_marker in time_markers:
        axs[1].axvline(x=time_marker, color='red', linestyle='--')

    # Annotate the lowest positive and largest negative derivatives
    annotation_text = ''
    if lowest_positive_derivative is not None:
        annotation_text += f'Lowest Positive Derivative: {lowest_positive_derivative:.4f}\n'
    else:
        annotation_text += 'Lowest Positive Derivative: None\n'

    if largest_negative_derivative is not None:
        annotation_text += f'Largest Negative Derivative: {largest_negative_derivative:.4f}'
    else:
        annotation_text += 'Largest Negative Derivative: None'

    fig.text(0.5, 0.02, annotation_text, ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    # Adjust layout
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Create the output directory for the current stim condition if it does not exist
    stim_output_dir = os.path.join(output_dir, f'd_events_{stim}')
    os.makedirs(stim_output_dir, exist_ok=True)

    # Save the figure to a file
    output_file = os.path.join(stim_output_dir, f'{bindist_file}.png')
    plt.savefig(output_file)
    plt.close(fig)
