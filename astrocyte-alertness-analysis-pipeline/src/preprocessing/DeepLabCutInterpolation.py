# DeepLabCutInterpolation.py
# -------------------------------------------------------------------------
# Origin: "Probability Interpolation.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   - Interpolates missing DeepLabCut keypoints using probability-weighted interpolation to produce smooth pupil and eye-gap trajectories.
#
# Inputs:
#   - CSV exported from DeepLabCut (per video)
#
# Outputs:
#   - Interpolated CSV with continuous keypoints
#
# File Relationships:
#   - Followed by PupilDiameterComputation for feature extraction.
#
# Dependencies:
#   - pandas, numpy, matplotlib.pyplot
# -------------------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the folder path containing the CSV files
folder_path = r"C:\Users\ASH213\Documents\Pupil activity"
output_folder_path = r"C:\Users\ASH213\Documents\Pupil activity"

os.makedirs(output_folder_path, exist_ok=True)

# Function to replace data with NaN based on likelihood and interpolate using linear method
def replace_and_interpolate(df, pupil, extended_indices):
    try:
        likelihood_col = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'likelihood')]
        x_col = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'x')]
        y_col = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'y')]

        # Identify indices where likelihood is below 0.95
        below_threshold_indices = likelihood_col[likelihood_col < 0.95].index

        # Extend the indices to include four points before and after
        for idx in below_threshold_indices:
            for offset in range(1, 6):  # Extend four points before and after
                if idx - offset >= 0:
                    extended_indices.add(idx - offset)
                if idx + offset < len(likelihood_col):
                    extended_indices.add(idx + offset)

        # Convert the set to a sorted list
        extended_indices = sorted(list(extended_indices))

        # Replace x and y with NaN at the extended indices
        df.loc[extended_indices, ('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'x')] = float('nan')
        df.loc[extended_indices, ('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'y')] = float('nan')

        # Interpolate the NaN values using linear interpolation
        df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'x')] = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'x')].interpolate(method='linear')
        df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'y')] = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', pupil, 'y')].interpolate(method='linear')
    except KeyError:
        print(f"Columns for {pupil} not found. Skipping interpolation.")

# Iterate through the folder and process each CSV file
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)

        # Read the CSV with multiple headers
        df = pd.read_csv(file_path, header=[0, 1, 2])

        extended_indices = set()
        # Replace and interpolate data for each pupil and accumulate indices
        for pupil in ['Top pupil', 'Bot pupil', 'Right pupil', 'Left pupil']:
            replace_and_interpolate(df, pupil, extended_indices)

        # Use the accumulated indices to replace and interpolate corners of eye
        replace_and_interpolate(df, 'Right corner of eye', extended_indices)
        replace_and_interpolate(df, 'Left corner of eye', extended_indices)

        # Save the DataFrame to a new CSV file
        output_file_path = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}_interpolated.csv")
        df.to_csv(output_file_path, index=False)

        # Extract the likelihood columns for plotting
        top_pupil_likelihood = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', 'Top pupil', 'likelihood')]
        bot_pupil_likelihood = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', 'Bot pupil', 'likelihood')]
        right_pupil_likelihood = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', 'Right pupil', 'likelihood')]
        left_pupil_likelihood = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', 'Left pupil', 'likelihood')]
        right_corner_likelihood = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', 'Right corner of eye', 'likelihood')]
        left_corner_likelihood = df[('DLC_resnet101_Pupil DialationMay1shuffle1_100000', 'Left corner of eye', 'likelihood')]

        # Create separate plots for each column
        plt.figure(figsize=(12, 8))

        # Plot for Top Pupil Likelihood
        plt.subplot(3, 2, 1)
        plt.plot(top_pupil_likelihood)
        plt.title('Top Pupil Likelihood')
        plt.xlabel('Frame')
        plt.ylabel('Likelihood')

        # Plot for Bot Pupil Likelihood
        plt.subplot(3, 2, 2)
        plt.plot(bot_pupil_likelihood)
        plt.title('Bot Pupil Likelihood')
        plt.xlabel('Frame')
        plt.ylabel('Likelihood')

        # Plot for Right Pupil Likelihood
        plt.subplot(3, 2, 3)
        plt.plot(right_pupil_likelihood)
        plt.title('Right Pupil Likelihood')
        plt.xlabel('Frame')
        plt.ylabel('Likelihood')

        # Plot for Left Pupil Likelihood
        plt.subplot(3, 2, 4)
        plt.plot(left_pupil_likelihood)
        plt.title('Left Pupil Likelihood')
        plt.xlabel('Frame')
        plt.ylabel('Likelihood')

        # Plot for Right corner Likelihood
        plt.subplot(3, 2, 5)
        plt.plot(right_corner_likelihood)
        plt.title('Right corner Likelihood')
        plt.xlabel('Frame')
        plt.ylabel('Likelihood')

        # Plot for Left corner Likelihood
        plt.subplot(3, 2, 6)
        plt.plot(left_corner_likelihood)
        plt.title('Left corner Likelihood')
        plt.xlabel('Frame')
        plt.ylabel('Likelihood')

        # Adjust layout and show the plot
        plt.tight_layout()
        plt.show()

        print(f"Processed and displayed: {filename}")

print("All files processed.")
