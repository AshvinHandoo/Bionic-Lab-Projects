"""
File: dilation_event_average_plotting.py
Origin: "Dilation event average plotting.py"
Category: Event detection & alignment
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

import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = r"C:\Users\ASH213\Documents\Correlated\890\stimcondition_4_averaged_results.csv"
data = pd.read_csv(file_path)

# Extract the necessary columns
pupil_diameter_ratio = data['Pupil Diameter Ratio']
pupil_diameter_ratio_std = data['Pupil Diameter Ratio Std']
calcium = data['calcium']
calcium_std = data['calcium Std']
index = data.index

# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot Pupil Diameter Ratio
ax1.plot(index, pupil_diameter_ratio, label='Pupil Diameter Ratio', color='blue')
ax1.fill_between(index, pupil_diameter_ratio - pupil_diameter_ratio_std,
                 pupil_diameter_ratio + pupil_diameter_ratio_std, color='blue', alpha=0.2)
ax1.set_xlabel('Index')
ax1.set_ylabel('Pupil Diameter Ratio', color='blue')
ax1.set_ylim([0, 1])
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis for the Calcium data
ax2 = ax1.twinx()
ax2.plot(index, calcium, label='Calcium', color='green')
ax2.fill_between(index, calcium - calcium_std, calcium + calcium_std, color='green', alpha=0.2)
ax2.set_ylabel('Calcium', color='green')
ax2.set_ylim([-0.5, 0.5])
ax2.tick_params(axis='y', labelcolor='green')

# Add legends
fig.tight_layout()
fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))

plt.title('Pupil Diameter Ratio and Calcium with Standard Deviation')
plt.show()
