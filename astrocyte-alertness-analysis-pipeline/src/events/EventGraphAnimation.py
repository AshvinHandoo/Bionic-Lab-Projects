# EventGraphAnimation.py
# -------------------------------------------------------------------------
# Origin: "Pupil event graph animation.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   Animates pupil ratio, calcium, and pupil derivative traces over time and
highlights threshold crossings.
#
# Inputs:
#   - Event detection CSV (e.g., bindist_2040.csv)
#
# Outputs:
#   - ~2-minute MP4/AVI animation of evolving traces
#
# File Relationships:
#   - Uses EventThresholdDetectionNormalized outputs.
#
# Dependencies:
#   matplotlib.animation, pandas, numpy
# -------------------------------------------------------------------------

import os
from matplotlib.animation import FFMpegWriter
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

# Set the path to the ffmpeg executable
os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\Users\ASH213\Documents\FFmpeg\bin"

# Base directory containing trials and stimconditions
base_dir = r"C:\Users\ASH213\Documents\Correlated\890\d084"

# Create the "animations" folder if it doesn't exist
animations_folder = os.path.join(base_dir, "animations")
os.makedirs(animations_folder, exist_ok=True)

# Traverse through each trial and stimcondition directory
for trial_dir in sorted(os.listdir(base_dir)):
    trial_path = os.path.join(base_dir, trial_dir)
    if os.path.isdir(trial_path):
        for stimcondition_dir in sorted(os.listdir(trial_path)):
            stimcondition_path = os.path.join(trial_path, stimcondition_dir)
            if os.path.isdir(stimcondition_path):
                # Look for bindist_2040.csv in each stimcondition directory
                csv_file = os.path.join(stimcondition_path, "bindist_2040.csv")
                if os.path.isfile(csv_file):
                    df = pd.read_csv(csv_file)

                    # Check if the required columns are present in the DataFrame
                    required_columns = ['Pupil Diameter Ratio', 'time', 'calcium', 'Pupil Diameter Ratio Derivative', 'threshold']
                    if all(column in df.columns for column in required_columns):
                        pupil_diameter_ratio = df['Pupil Diameter Ratio']
                        calcium = df['calcium']
                        pupil_diameter_ratio_derivative = df['Pupil Diameter Ratio Derivative']
                        threshold = df['threshold']

                        # Create a figure and axes for the three separate plots
                        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

                        # Set up the first plot for Pupil Diameter Ratio
                        ax1.set_xlim([0, len(pupil_diameter_ratio) - 1])
                        ax1.set_ylim([0, 1])
                        animated_plot_pupil, = ax1.plot([], [], lw=2, label='Pupil Diameter Ratio', color='blue')
                        ax1.set_xlabel('Index')
                        ax1.set_ylabel('Pupil Diameter Ratio', color='blue')
                        ax1.tick_params(axis='y', labelcolor='blue')

                        # Set up the second plot for calcium
                        abs_max_calcium = max(abs(calcium.min()), abs(calcium.max()))
                        y_lim_calcium = [-0.05, 0.05] if abs_max_calcium <= 0.05 else [-abs_max_calcium, abs_max_calcium]
                        ax2.set_xlim([0, len(calcium) - 1])
                        ax2.set_ylim(y_lim_calcium)
                        animated_plot_calcium, = ax2.plot([], [], lw=2, label='Calcium', color='red')
                        ax2.set_xlabel('Index')
                        ax2.set_ylabel('Calcium', color='red')
                        ax2.tick_params(axis='y', labelcolor='red')

                        # Set up the third plot for Pupil Diameter Ratio Derivative
                        abs_max_derivative = max(abs(pupil_diameter_ratio_derivative.min()), abs(pupil_diameter_ratio_derivative.max()))
                        y_lim_derivative = [-0.5, 0.5] if abs_max_derivative <= 0.5 else [-abs_max_derivative, abs_max_derivative]
                        ax3.set_xlim([0, len(pupil_diameter_ratio_derivative) - 1])
                        ax3.set_ylim(y_lim_derivative)
                        animated_plot_derivative, = ax3.plot([], [], lw=2, label='Pupil Diameter Ratio Derivative', color='green')
                        ax3.set_xlabel('Index')
                        ax3.set_ylabel('Pupil Diameter Ratio Derivative', color='green')
                        ax3.tick_params(axis='y', labelcolor='green')

                        # Identify indices where threshold is "yes"
                        threshold_indices = df.index[df['threshold'] == 'yes'].tolist()

                        # Add threshold lines to all plots without adding them to the legend
                        for idx in threshold_indices:
                            ax1.axvline(x=idx, color='red', linestyle='--', lw=0.5, label='_nolegend_')
                            ax2.axvline(x=idx, color='red', linestyle='--', lw=0.5, label='_nolegend_')
                            ax3.axvline(x=idx, color='red', linestyle='--', lw=0.5, label='_nolegend_')

                        def init():
                            animated_plot_pupil.set_data([], [])
                            animated_plot_calcium.set_data([], [])
                            animated_plot_derivative.set_data([], [])
                            return animated_plot_pupil, animated_plot_calcium, animated_plot_derivative

                        def update_data(frame):
                            frame //= 3  # Add every 3 frames
                            max_length = len(pupil_diameter_ratio)
                            if frame > max_length:
                                frame = max_length
                            x = range(frame)
                            y_pupil = pupil_diameter_ratio[:frame]
                            y_calcium = calcium[:frame]
                            y_derivative = pupil_diameter_ratio_derivative[:frame]
                            animated_plot_pupil.set_data(x, y_pupil)
                            animated_plot_calcium.set_data(x, y_calcium)
                            animated_plot_derivative.set_data(x, y_derivative)
                            return animated_plot_pupil, animated_plot_calcium, animated_plot_derivative

                        total_frames = 3600
                        animation = FuncAnimation(fig, update_data, frames=total_frames, init_func=init, interval=1000/30, blit=True)

                        # Adding legends
                        ax1.legend(loc='upper right')
                        ax2.legend(loc='upper right')
                        ax3.legend(loc='upper right')

                        # Save the animation as an MP4 file in the "animations" folder
                        save_filename = f"animation_{trial_dir}_{stimcondition_dir}.mp4"
                        save_path = os.path.join(animations_folder, save_filename)
                        writer = FFMpegWriter(fps=30, metadata=dict(artist='Me'), bitrate=1800)
                        animation.save(save_path, writer=writer)

                        # Close the plot to free memory
                        plt.close(fig)

                    else:
                        print(f"Required columns are not present in the CSV file: {csv_file}")
