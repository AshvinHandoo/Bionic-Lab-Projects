"""
File: pupil_event_videoplayer_preparer.py
Origin: "Pupil event videoplayer preparer.py"
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

import os
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

# Define the paths to the input folders
folder1 = r"C:\Users\ASH213\Documents\Correlated\890\d084\animations"
folder2 = r"C:\Users\ASH213\Documents\Correlated\890\d084\videos for animations"

# Define the output folder
output_folder = r"C:\Users\ASH213\Documents\Correlated\890\d084\dual video playing"

# Define the target duration (2 minutes)
target_duration = 2 * 60  # 2 minutes in seconds


def process_videos(input_folder, output_folder, prefix):
    # Iterate over all video files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(input_folder, filename)
            video = VideoFileClip(video_path)

            # Calculate the speed factor
            factor = video.duration / target_duration

            # Adjust the speed of the video
            adjusted_video = video.fx(vfx.speedx, factor).set_duration(target_duration)

            # Create the output file path
            output_path = os.path.join(output_folder, f"{prefix}_{filename}")

            # Save the adjusted video
            adjusted_video.write_videofile(output_path)


# Process videos in both folders
process_videos(folder1, output_folder, "f")
process_videos(folder2, output_folder, "f")
