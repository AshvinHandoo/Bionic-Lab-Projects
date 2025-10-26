"""
File: time_of_derivative.py
Origin: "Time of derivative.py"
Category: Analytical routines & statistics
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
import numpy as np
import matplotlib.pyplot as plt


def find_max_positive_derivative(csv_file):
    # Load the data from the CSV file
    data = pd.read_csv(csv_file)

    # Ensure the CSV contains the required columns
    if not {'time', 'Pupil Diameter Ratio', 'calcium'}.issubset(data.columns):
        raise ValueError("CSV file must contain 'time', 'Pupil Diameter Ratio', and 'calcium' columns")

    # Compute the derivative of the Pupil Diameter Ratio with respect to time
    data['Derivative'] = np.gradient(data['Pupil Diameter Ratio'], data['time'])

    # Find the maximum positive derivative
    max_positive_derivative = data['Derivative'].max()

    # Find the corresponding calcium level and time
    max_derivative_row = data.loc[data['Derivative'].idxmax()]

    time_at_max_derivative = max_derivative_row['time']
    calcium_at_max_derivative = max_derivative_row['calcium']

    return max_positive_derivative, time_at_max_derivative, calcium_at_max_derivative


def find_max_negative_derivative(csv_file):
    # Load the data from the CSV file
    data = pd.read_csv(csv_file)

    # Ensure the CSV contains the required columns
    if not {'time', 'Pupil Diameter Ratio', 'calcium'}.issubset(data.columns):
        raise ValueError("CSV file must contain 'time', 'Pupil Diameter Ratio', and 'calcium' columns")

    # Compute the derivative of the Pupil Diameter Ratio with respect to time
    data['Derivative'] = np.gradient(data['Pupil Diameter Ratio'], data['time'])

    # Find the maximum negative derivative
    max_negative_derivative = data['Derivative'].min()

    # Find the corresponding calcium level and time
    min_derivative_row = data.loc[data['Derivative'].idxmin()]

    time_at_min_derivative = min_derivative_row['time']
    calcium_at_min_derivative = min_derivative_row['calcium']

    return max_negative_derivative, time_at_min_derivative, calcium_at_min_derivative


def process_folders(base_folder):
    pos_results = []
    neg_results = []

    # Iterate through the folders and subfolders
    for trial_folder in os.listdir(base_folder):
        trial_path = os.path.join(base_folder, trial_folder)
        if os.path.isdir(trial_path):
            for stim_folder in os.listdir(trial_path):
                stim_path = os.path.join(trial_path, stim_folder)
                if os.path.isdir(stim_path):
                    csv_file = os.path.join(stim_path, 'bindist_2000.csv')
                    if os.path.exists(csv_file):
                        try:
                            max_pos_derivative, pos_time, pos_calcium = find_max_positive_derivative(csv_file)
                            pos_results.append({
                                'trial': trial_folder,
                                'stim_condition': stim_folder,
                                'time': pos_time,
                                'calcium': pos_calcium
                            })
                            max_neg_derivative, neg_time, neg_calcium = find_max_negative_derivative(csv_file)
                            neg_results.append({
                                'trial': trial_folder,
                                'stim_condition': stim_folder,
                                'time': neg_time,
                                'calcium': neg_calcium
                            })
                        except Exception as e:
                            print(f"Error processing {csv_file}: {e}")

    return pos_results, neg_results


def plot_results(results, output_folder, plot_name):
    # Define colors for each stim condition
    stim_conditions = sorted(set(result['stim_condition'] for result in results))
    colors = plt.cm.jet(np.linspace(0, 1, len(stim_conditions)))
    stim_condition_colors = dict(zip(stim_conditions, colors))

    plt.figure(figsize=(10, 6))

    # Plot the results
    plotted_conditions = set()
    for result in results:
        plt.scatter(result['time'], result['calcium'],
                    color=stim_condition_colors[result['stim_condition']], alpha=0.6)
        plt.text(result['time'], result['calcium'], result['trial'][-1], fontsize=9, ha='right')
        if result['stim_condition'] not in plotted_conditions:
            plt.scatter([], [], color=stim_condition_colors[result['stim_condition']], label=result['stim_condition'])
            plotted_conditions.add(result['stim_condition'])

    # Create a legend for stim conditions
    plt.legend(title="Stim Conditions")

    plt.xlabel('Time')
    plt.ylabel('Calcium')
    plt.title(f'Calcium Levels at {plot_name} Over Time')

    # Save the plot
    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(os.path.join(output_folder, f'{plot_name.replace(" ", "_").lower()}.png'))
    plt.close()


# Example usage
base_folder = r'C:\Users\ASH213\Documents\Correlated\890\d070'  # Replace with the path to your base folder
pos_results, neg_results = process_folders(base_folder)

# Print results
print("Positive Derivative Results:")
for result in pos_results:
    print(f"Trial: {result['trial']}, Stim Condition: {result['stim_condition']}, "
          f"Time: {result['time']}, Calcium: {result['calcium']}")

print("\nNegative Derivative Results:")
for result in neg_results:
    print(f"Trial: {result['trial']}, Stim Condition: {result['stim_condition']}, "
          f"Time: {result['time']}, Calcium: {result['calcium']}")

# Plot the results
output_folder = r'C:\Users\ASH213\Documents\Correlated\890\d070\time_of_max_derivative_graphs'
plot_results(pos_results, output_folder, "Maximum Positive Derivative")
plot_results(neg_results, output_folder, "Maximum Negative Derivative")