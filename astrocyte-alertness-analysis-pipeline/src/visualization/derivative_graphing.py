"""
File: derivative_graphing.py
Origin: "Derivative graphing.py"
Category: Plotting & visualization utilities
Author: Ashvin Handoo
Last Updated: 2025-10-26

Summary:
    Part of the astrocyte-alertness-analysis-pipeline. This module was renamed and
    lightly documented for clarity and recruiter readability.

Notes for Reviewers:
    • Original logic preserved; variable naming and comments minimally cleaned.
    • Data paths may be set via CLI args or environment variables.
    • See README for synthetic data demo and end-to-end run instructions.

"""


# ---- Original script content below ----

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Base directory where t1, t2, t3 folders are located
base_dir = r"C:\Users\ASH213\Documents\Correlated\890\d084"

# Subfolders for each stim condition
stim_conditions = ['stimcondition_1', 'stimcondition_2', 'stimcondition_3', 'stimcondition_4', 'stimcondition_5']

# Timepoints
timepoints = ['trial_1', 'trial_2', 'trial_3']

output_dir = r'C:\Users\ASH213\Documents\Correlated\890\d084'

# Iterate over each stim condition
for stim in stim_conditions:
    # Find all bindist_* files in the first timepoint's stimcondition folder to get all unique bindist_* names
    bindist_files = os.listdir(os.path.join(base_dir, timepoints[0], stim))
    bindist_files = [file for file in bindist_files if file.startswith('bindist_')]

    # Iterate over each bindist_* file
    for bindist_file in bindist_files:
        fig, axs = plt.subplots(3, len(timepoints) + 1, figsize=(20, 15))
        fig.suptitle(f'Graphs for {stim} - {bindist_file}', fontsize=16)

        pupil_derivative_data = []
        calcium_activity_data = []
        time_data = []

        # First pass: collect all Pupil Diameter Ratio data and compute derivatives
        for t in timepoints:
            csv_path = os.path.join(base_dir, t, stim, bindist_file)
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                pupil_diameter_ratio = df['Pupil Diameter Ratio']
                time = df['time']

                # Compute the derivative of the Pupil Diameter Ratio
                pupil_derivative = np.gradient(pupil_diameter_ratio, time)
                pupil_derivative_data.append(pupil_derivative)

        if not pupil_derivative_data:
            print(f"No Pupil Diameter Ratio data found for {bindist_file} in {stim}")
            continue

        # Calculate the average Pupil Diameter Ratio derivative across all timepoints
        avg_pupil_derivative_overall = np.mean([item for sublist in pupil_derivative_data for item in sublist])

        # Clear the lists to recollect data for plotting
        pupil_derivative_data = []
        calcium_activity_data = []
        time_data = []

        # Second pass: plot the data and collect the new Pupil Diameter Ratio derivative values
        for j, t in enumerate(timepoints):
            csv_path = os.path.join(base_dir, t, stim, bindist_file)
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)

                # Determine y-axis limits for calcium activity
                abs_max_calcium = max(abs(df['calcium'].min()), abs(df['calcium'].max()))
                if abs_max_calcium > 0.05:
                    y_lim_calcium = (-abs_max_calcium, abs_max_calcium)
                else:
                    y_lim_calcium = (-0.05, 0.05)

                # Plot time vs calcium activity
                axs[0, j].plot(df['time'], df['calcium'], label=f'{t}')
                axs[0, j].set_title(f'{t} - Calcium Activity')
                axs[0, j].set_xlabel('Time')
                axs[0, j].set_ylabel('Calcium Activity')
                axs[0, j].set_ylim(y_lim_calcium)

                pupil_diameter_ratio = df['Pupil Diameter Ratio']
                time = df['time']

                # Compute the derivative of the Pupil Diameter Ratio
                pupil_derivative = np.gradient(pupil_diameter_ratio, time)

                # Determine y-axis limits for Pupil Diameter Ratio derivative
                abs_max_pupil_derivative = max(abs(pupil_derivative.min()), abs(pupil_derivative.max()))
                if abs_max_pupil_derivative > 1:
                    y_lim_pupil_derivative = (-abs_max_pupil_derivative, abs_max_pupil_derivative)
                else:
                    y_lim_pupil_derivative = (-0.5, 0.5)

                # Plot time vs Pupil Diameter Ratio derivative
                axs[1, j].plot(time, pupil_derivative, label=f'{t}')
                axs[1, j].set_title(f'{t} - Pupil Diameter Ratio Derivative')
                axs[1, j].set_xlabel('Time')
                axs[1, j].set_ylabel('Pupil Diameter Ratio Derivative')
                axs[1, j].set_ylim(y_lim_pupil_derivative)  # Set dynamic y-axis limits for Pupil Diameter Ratio derivative

                # Collect data for averaging
                pupil_derivative_data.append(pupil_derivative)
                calcium_activity_data.append(df['calcium'].values[:len(pupil_derivative)])
                time_data.append(time.values[:len(pupil_derivative)])

                # Plot time vs calcium activity and Pupil Diameter Ratio derivative on the same graph using twinx for second y-axis
                ax2 = axs[2, j].twinx()
                axs[2, j].plot(time, df['calcium'][:len(pupil_derivative)], label='Calcium Activity', color='b')
                ax2.plot(time, pupil_derivative, label='Pupil Diameter Ratio Derivative', color='r')
                axs[2, j].set_title(f'{t} - Calcium Activity & Pupil Diameter Ratio Derivative')
                axs[2, j].set_xlabel('Time')
                axs[2, j].set_ylabel('Calcium Activity')
                ax2.set_ylabel('Pupil Diameter Ratio Derivative')
                axs[2, j].set_ylim(y_lim_calcium)  # Set dynamic y-axis limits for calcium activity in combined graph
                ax2.set_ylim(y_lim_pupil_derivative)  # Set dynamic y-axis limits for Pupil Diameter Ratio derivative in combined graph
                axs[2, j].legend(loc='upper left')
                ax2.legend(loc='upper right')

        if pupil_derivative_data and calcium_activity_data:
            # Ensure all arrays have the same length
            min_length = min(map(len, pupil_derivative_data + calcium_activity_data + time_data))
            pupil_derivative_data = [data[:min_length] for data in pupil_derivative_data]
            calcium_activity_data = [data[:min_length] for data in calcium_activity_data]
            time = time_data[0][:min_length]  # Use the 'time' column trimmed to the min length

            # Calculate average and standard deviation of the Pupil Diameter Ratio derivative and calcium activity
            avg_pupil_derivative = np.mean(pupil_derivative_data, axis=0)
            std_pupil_derivative = np.std(pupil_derivative_data, axis=0)
            avg_calcium_activity = np.mean(calcium_activity_data, axis=0)
            std_calcium_activity = np.std(calcium_activity_data, axis=0)

            # Determine y-axis limits for average calcium activity
            abs_max_calcium_avg = max(abs(avg_calcium_activity.min()), abs(avg_calcium_activity.max()))
            if abs_max_calcium_avg > 0.05:
                y_lim_avg_calcium = (-abs_max_calcium_avg, abs_max_calcium_avg)
            else:
                y_lim_avg_calcium = (-0.05, 0.05)

            # Determine y-axis limits for average Pupil Diameter Ratio derivative
            abs_max_pupil_derivative_avg = max(abs(avg_pupil_derivative.min()), abs(avg_pupil_derivative.max()))
            if abs_max_pupil_derivative_avg > 1:
                y_lim_avg_pupil_derivative = (-abs_max_pupil_derivative_avg, abs_max_pupil_derivative_avg)
            else:
                y_lim_avg_pupil_derivative = (-0.5, 0.5)

            # Plot average calcium activity with standard deviation
            axs[0, -1].plot(time, avg_calcium_activity, label='Average')
            axs[0, -1].fill_between(time, avg_calcium_activity - std_calcium_activity, avg_calcium_activity + std_calcium_activity, color='b', alpha=0.2)
            axs[0, -1].set_title('Average Calcium Activity')
            axs[0, -1].set_xlabel('Time')
            axs[0, -1].set_ylabel('Calcium Activity')
            axs[0, -1].set_ylim(y_lim_avg_calcium)  # Set y-axis limits for calcium activity
            axs[0, -1].legend()

            # Plot average of Pupil Diameter Ratio derivative with standard deviation
            axs[1, -1].plot(time, avg_pupil_derivative, label='Average')
            axs[1, -1].fill_between(time, avg_pupil_derivative - std_pupil_derivative, avg_pupil_derivative + std_pupil_derivative, color='b', alpha=0.2)
            axs[1, -1].set_title('Average Pupil Diameter Ratio Derivative')
            axs[1, -1].set_xlabel('Time')
            axs[1, -1].set_ylabel('Pupil Diameter Ratio Derivative')
            axs[1, -1].set_ylim(y_lim_avg_pupil_derivative)  # Set y-axis limits for Pupil Diameter Ratio derivative
            axs[1, -1].legend()

            # Plot average calcium activity and average Pupil Diameter Ratio derivative on the same graph using twinx for second y-axis
            ax2 = axs[2, -1].twinx()
            axs[2, -1].plot(time, avg_calcium_activity, label='Average Calcium Activity', color='b')
            ax2.plot(time, avg_pupil_derivative, label='Average Pupil Diameter Ratio Derivative', color='r')
            axs[2, -1].set_title('Average Calcium Activity & Average Pupil Diameter Ratio Derivative')
            axs[2, -1].set_xlabel('Time')
            axs[2, -1].set_ylabel('Calcium Activity')
            ax2.set_ylabel('Pupil Diameter Ratio Derivative')
            axs[2, -1].set_ylim(y_lim_avg_calcium)  # Set dynamic y-axis limits for average calcium activity in combined graph
            ax2.set_ylim(y_lim_avg_pupil_derivative)  # Set dynamic y-axis limits for average Pupil Diameter Ratio derivative in combined graph
            axs[2, -1].legend(loc='upper left')
            ax2.legend(loc='upper right')

        # Adjust layout
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Create the output directory for the current stim condition if it does not exist
        stim_output_dir = os.path.join(output_dir, f'd_{stim}')
        os.makedirs(stim_output_dir, exist_ok=True)

        # Save the figure to a file
        output_file = os.path.join(stim_output_dir, f'{bindist_file}.png')
        plt.savefig(output_file)
        plt.close(fig)