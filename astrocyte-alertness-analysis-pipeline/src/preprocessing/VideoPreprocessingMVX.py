# VideoPreprocessingMVX.py
# -------------------------------------------------------------------------
# Origin: "Video preprocess MVX.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   - Preprocesses MVX videos containing multiple stimulation conditions; produces reliable clips for DeepLabCut.
#
# Inputs:
#   - Raw MVX video (.h264)
#
# Outputs:
#   - Preprocessed video file for DLC
#
# File Relationships:
#   - Upstream of DeepLabCutInterpolation and PupilDiameterComputation.
#
# Dependencies:
#   - cv2 (OpenCV), os
# -------------------------------------------------------------------------

import cv2
import os

input_folder_path = "C:/Users/ASH213/Documents/Pupil vids/rawMVXvids"
output_folder_path_sliced = "C:/Users/ASH213/Documents/Pupil vids/nontrimmedMVXvids"
output_folder_path_nonsliced = "C:/Users/ASH213/Documents/Pupil vids/processedMVXvids"

os.makedirs(output_folder_path_sliced, exist_ok=True)
os.makedirs(output_folder_path_nonsliced, exist_ok=True)

# Get a list of all video files in the input folder
video_files = [f for f in os.listdir(input_folder_path) if f.endswith('.h264')]

for video_file in video_files:
    # Check if 'test' is present in the video title
    if 'test' in video_file:
        continue

    # Check if the video length is under 60 MB
    video_length = os.path.getsize(os.path.join(input_folder_path, video_file))
    if video_length < 60 * 1024 * 1024:
        continue

    # Input and output video paths
    input_video_path = os.path.join(input_folder_path, video_file)

    # Open the original video file
    cap = cv2.VideoCapture(input_video_path)

    # Get the video frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Initialize variables for output video
    out = None
    video_counter = 1

    framemean = []
    consecutive_low_derivative_frames = 0
    threshold_consecutive_low_derivative_frames = 150  # Adjust this threshold as needed
    derivative_threshold = 1.4  # Adjust this threshold as needed

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            break

        # Convert the entire frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Define the region of interest (a box in the middle towards the bottom)
        box_width = frame_width // 3
        box_height = frame_height // 5
        box_x = (frame_width - box_width) // 2  # Center the box horizontally
        box_y = frame_height - box_height      # Align the box with the bottom of the frame

        # Select the box region
        box_region = gray[box_y:box_y + box_height, box_x:box_x + box_width]

        # Calculate the mean intensity of the selected portion
        framemean.append(box_region.mean())

        # Apply CLAHE to enhance contrast
        clahe = cv2.createCLAHE(clipLimit=7.0, tileGridSize=(7, 7))
        clahe_img = clahe.apply(gray)

        # Check if 'tbs' or 'Hz' are present in the video title or if video is less than 160 MB
        if 'tbs' in video_file or 'Hz' in video_file or video_length < 160 * 1024 * 1024:
            # Just write the modified frame to the nonsliced output video
            if out is None:
                # Start writing to a new output video file
                output_path = os.path.join(output_folder_path_nonsliced, f'{video_file.split(".")[0]}_{video_counter}.mp4')
                out = cv2.VideoWriter(output_path, fourcc, 30, (frame_width, frame_height), isColor=False)
                video_counter += 1
            out.write(clahe_img)
        else:
            # Calculate the derivative magnitude
            if len(framemean) > 1:
                derivative_magnitude = abs(framemean[-1] - framemean[-2])

                # Check if the derivative magnitude is below the threshold
                if derivative_magnitude < derivative_threshold:
                    consecutive_low_derivative_frames += 1
                else:
                    consecutive_low_derivative_frames = 0

                # Write the modified frame to the output video if the derivative magnitude is above the threshold
                if consecutive_low_derivative_frames <= threshold_consecutive_low_derivative_frames:
                    if out is None:
                        # Start writing to a new output video file
                        output_path = os.path.join(output_folder_path_sliced, f'{video_file.split(".")[0]}_{video_counter}.mp4')
                        out = cv2.VideoWriter(output_path, fourcc, 30, (frame_width, frame_height), isColor=False)
                        video_counter += 1
                    out.write(clahe_img)
                else:
                    if out is not None:
                        # Release the current output video file
                        out.release()
                        out = None
                        framemean = []  # Reset framemean for the next video

    # Release the video capture object
    cap.release()
    if out is not None:
        out.release()  # Ensure to release the last video file if it was not released inside the loop

print("Processing complete.")
