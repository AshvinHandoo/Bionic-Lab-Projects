# DualVideoPlayer.py
# -------------------------------------------------------------------------
# Origin: "Dual videoplayer.py"
# Last Updated: 2025-10-27
#
# Purpose:
#   - Displays two synchronized videos side by side (e.g., calcium and pupil) allowing user to scrub and review temporal alignment interactively.
#
# Inputs:
#   - Two preprocessed video files
#
# Outputs:
#   - Interactive playback window
#
# File Relationships:
#   - Standalone visualization utility.
#
# Dependencies:
#   - cv2 (OpenCV), tkinter, PIL (Pillow)
# -------------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, Scale
import cv2
from PIL import Image, ImageTk

class DualVideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual Video Player")

        self.cap1 = None
        self.cap2 = None
        self.playing = False

        self.panel1 = tk.Label(root)
        self.panel1.pack(side="left", padx=10, pady=10)

        self.panel2 = tk.Label(root)
        self.panel2.pack(side="right", padx=10, pady=10)

        self.slider = Scale(root, from_=0, to=100, orient="horizontal", command=self.scrub)
        self.slider.pack(fill="x", padx=10, pady=10)

        btn_load1 = tk.Button(root, text="Load Video 1", command=self.load_video1)
        btn_load1.pack(side="left", padx=10, pady=10)

        btn_load2 = tk.Button(root, text="Load Video 2", command=self.load_video2)
        btn_load2.pack(side="right", padx=10, pady=10)

        btn_play = tk.Button(root, text="Play/Pause", command=self.toggle_play)
        btn_play.pack(fill="x", padx=10, pady=10)

    def load_video1(self):
        video_path = filedialog.askopenfilename()
        if video_path:
            self.cap1 = cv2.VideoCapture(video_path)
            self.update_slider_range()

    def load_video2(self):
        video_path = filedialog.askopenfilename()
        if video_path:
            self.cap2 = cv2.VideoCapture(video_path)
            self.update_slider_range()

    def update_slider_range(self):
        if self.cap1 and self.cap2:
            total_frames1 = int(self.cap1.get(cv2.CAP_PROP_FRAME_COUNT))
            total_frames2 = int(self.cap2.get(cv2.CAP_PROP_FRAME_COUNT))
            self.slider.config(to=min(total_frames1, total_frames2))

    def get_video_fps(self, cap):
        return cap.get(cv2.CAP_PROP_FPS)

    def toggle_play(self):
        self.playing = not self.playing
        if self.playing:
            fps1 = self.get_video_fps(self.cap1)
            fps2 = self.get_video_fps(self.cap2)
            # Use the minimum fps of both videos to avoid skipping frames
            self.fps = min(fps1, fps2)
            self.play_videos()

    def play_videos(self):
        if not self.playing:
            return

        ret1, frame1 = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        if ret1 and ret2:
            self.display_frame(self.panel1, frame1)
            self.display_frame(self.panel2, frame2)
            self.slider.set(self.slider.get() + 1)

        delay = int(1000 / self.fps)  # Convert fps to milliseconds
        self.root.after(delay, self.play_videos)

    def display_frame(self, panel, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        panel.configure(image=frame)
        panel.image = frame

    def scrub(self, value):
        frame_number = int(value)
        if self.cap1 and self.cap2:
            self.cap1.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            self.cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            if ret1 and ret2:
                self.display_frame(self.panel1, frame1)
                self.display_frame(self.panel2, frame2)

if __name__ == "__main__":
    root = tk.Tk()
    player = DualVideoPlayer(root)
    root.mainloop()
