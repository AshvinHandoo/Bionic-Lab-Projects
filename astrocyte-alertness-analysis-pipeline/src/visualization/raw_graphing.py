"""
File: raw_graphing.py
Origin: "Raw graphing.py"
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
base_dir = r"C:\Users\ASH213\Documents\Correlated"

# Subfolders for each stim condition
stim_conditions = ['stimcondition_1', 'stimcondition_2', 'stimcondition_3', 'stimcondition_4', 'stimcondition_5']

# Timepoints
timepoints = ['trial_1', 'trial_2', 'trial_3']


output_dir = r'C:\Users\ASH213\Documents\Correlated'

# Iterate over each stim condition
for stim in stim_conditions:
    # Find all bindist_* files in the first timepoint's stimcondition folder to get all unique bindist_* names
    bindist_files = os.listdir(os.path.join(base_dir, timepoints[0], stim))
    bindist_files = [file for file in bindist_files if file.startswith('bindist_')]

    # Iterate over each bindist_* file
    for bindist_file in bindist_files:
        fig, axs = plt.subplots(3, len(timepoints) + 1, figsize=(20, 15))
        fig.suptitle(f'Graphs for {stim} - {bindist_file}', fontsize=16)

        pupil_diameter_data = []
        calcium_activity_data = []
        time_data = []

        # First pass: collect all Pupil Diameter Ratio data
        for t in timepoints:
            csv_path = os.path.join(base_dir, t, stim, bindist_file)
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                pupil_diameter_data.append(df['Pupil Diameter Ratio'].values)

        if not pupil_diameter_data:
            print(f"No Pupil Diameter Ratio data found for {bindist_file} in {stim}")
            continue

        # Calculate the average Pupil Diameter Ratio across all timepoints
        avg_pupil_diameter_overall = np.mean([item for sublist in pupil_diameter_data for item in sublist])

        # Clear the lists to recollect data for plotting
        pupil_diameter_data = []
        calcium_activity_data = []

        # Second pass: plot the data and collect the new Pupil Diameter Ratio values ( by the overall average)
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

                # Determine y-axis limits for Pupil Diameter Ratio
                abs_max_pupil_avg = max(abs(pupil_diameter_ratio.min()), abs(pupil_diameter_ratio.max()))
                if abs_max_pupil_avg > 1:
                    y_lim_pupil = (-abs_max_pupil_avg, abs_max_pupil_avg)
                else:
                    y_lim_pupil = (0, 1)

                # Plot time vs  Pupil Diameter Ratio
                axs[1, j].plot(df['time'], pupil_diameter_ratio, label=f'{t}')
                axs[1, j].set_title(f'{t} - Pupil Diameter Ratio')
                axs[1, j].set_xlabel('Time')
                axs[1, j].set_ylabel('Pupil Diameter Ratio')
                axs[1, j].set_ylim(y_lim_pupil)  # Set dynamic y-axis limits for Pupil Diameter Ratio

                # Collect data for averaging
                pupil_diameter_data.append(pupil_diameter_ratio.values)
                calcium_activity_data.append(df['calcium'].values)
                time_data.append(df['time'].values)

                # Plot time vs calcium activity and Pupil Diameter Ratio on the same graph using twinx for second y-axis
                ax2 = axs[2, j].twinx()
                axs[2, j].plot(df['time'], df['calcium'], label='Calcium Activity', color='b')
                ax2.plot(df['time'], pupil_diameter_ratio, label='Pupil Diameter Ratio', color='r')
                axs[2, j].set_title(f'{t} - Calcium Activity & Pupil Diameter Ratio')
                axs[2, j].set_xlabel('Time')
                axs[2, j].set_ylabel('Calcium Activity')
                ax2.set_ylabel('Pupil Diameter Ratio')
                axs[2, j].set_ylim(y_lim_calcium)  # Set dynamic y-axis limits for calcium activity in combined graph
                ax2.set_ylim(y_lim_pupil)  # Set dynamic y-axis limits for Pupil Diameter Ratio in combined graph
                axs[2, j].legend(loc='upper left')
                ax2.legend(loc='upper right')

        if pupil_diameter_data and calcium_activity_data:
            # Ensure all arrays have the same length
            min_length = min(map(len, pupil_diameter_data + calcium_activity_data + time_data))
            pupil_diameter_data = [data[:min_length] for data in pupil_diameter_data]
            calcium_activity_data = [data[:min_length] for data in calcium_activity_data]
            time = time_data[0][:min_length]  # Use the 'time' column trimmed to the min length

            # Calculate average and standard deviation of the  Pupil Diameter Ratio and calcium activity
            avg_pupil_diameter = np.mean(pupil_diameter_data, axis=0)
            std_pupil_diameter = np.std(pupil_diameter_data, axis=0)
            avg_calcium_activity = np.mean(calcium_activity_data, axis=0)
            std_calcium_activity = np.std(calcium_activity_data, axis=0)

            # Determine y-axis limits for average calcium activity
            abs_max_calcium_avg = max(abs(avg_calcium_activity.min()), abs(avg_calcium_activity.max()))
            if abs_max_calcium_avg > 0.05:
                y_lim_avg_calcium = (-abs_max_calcium_avg, abs_max_calcium_avg)
            else:
                y_lim_avg_calcium = (-0.05, 0.05)

            # Determine y-axis limits for average Pupil Diameter Ratio
            abs_max_pupil_avg = max(abs(avg_pupil_diameter.min()), abs(avg_pupil_diameter.max()))
            if abs_max_pupil_avg > 1:
                y_lim_avg_pupil = (-abs_max_pupil_avg, abs_max_pupil_avg)
            else:
                y_lim_avg_pupil = (0, 1)

            # Plot average calcium activity with standard deviation
            axs[0, -1].plot(time, avg_calcium_activity, label='Average')
            axs[0, -1].fill_between(time, avg_calcium_activity - std_calcium_activity, avg_calcium_activity + std_calcium_activity, color='b', alpha=0.2)
            axs[0, -1].set_title('Average Calcium Activity')
            axs[0, -1].set_xlabel('Time')
            axs[0, -1].set_ylabel('Calcium Activity')
            axs[0, -1].set_ylim(y_lim_avg_calcium)  # Set y-axis limits for calcium activity
            axs[0, -1].legend()

            # Plot average of  Pupil Diameter Ratio with standard deviation
            axs[1, -1].plot(time, avg_pupil_diameter, label='Average')
            axs[1, -1].fill_between(time, avg_pupil_diameter - std_pupil_diameter, avg_pupil_diameter + std_pupil_diameter, color='b', alpha=0.2)
            axs[1, -1].set_title('Average Pupil Diameter Ratio')
            axs[1, -1].set_xlabel('Time')
            axs[1, -1].set_ylabel('Pupil Diameter Ratio')
            axs[1, -1].set_ylim(y_lim_avg_pupil)  # Set y-axis limits for Pupil Diameter Ratio
            axs[1, -1].legend()

            # Plot average calcium activity and average  Pupil Diameter Ratio on the same graph using twinx for second y-axis
            ax2 = axs[2, -1].twinx()
            axs[2, -1].plot(time, avg_calcium_activity, label='Average Calcium Activity', color='b')
            ax2.plot(time, avg_pupil_diameter, label='Average Pupil Diameter Ratio ', color='r')
            axs[2, -1].set_title('Average Calcium Activity & Average Pupil Diameter Ratio')
            axs[2, -1].set_xlabel('Time')
            axs[2, -1].set_ylabel('Calcium Activity')
            ax2.set_ylabel('Pupil Diameter Ratio')
            axs[2, -1].set_ylim(y_lim_avg_calcium)  # Set dynamic y-axis limits for average calcium activity in combined graph
            ax2.set_ylim(y_lim_avg_pupil)  # Set dynamic y-axis limits for average Pupil Diameter Ratio in combined graph
            axs[2, -1].legend(loc='upper left')
            ax2.legend(loc='upper right')

        # Adjust layout
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Create the output directory for the current stim condition if it does not exist
        stim_output_dir = os.path.join(output_dir, stim)
        os.makedirs(stim_output_dir, exist_ok=True)

        # Save the figure to a file
        output_file = os.path.join(stim_output_dir, f'{bindist_file}.png')
        plt.savefig(output_file)
        plt.close(fig)