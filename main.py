import streamlit as st
import tempfile
import cv2
import os

from Tools.Backend import BackEnd
from Tools.FrontEnd import FrontEnd


st.title("Detect Traffic Violation")


FE = st.empty()
FE_2 = st.empty()

video_file = st.file_uploader("Tải video lên", type=["mp4", "avi", "mov"])

if video_file is not None:

    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(video_file.read())

    cap = cv2.VideoCapture(temp_video.name)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break 

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi màu OpenCV (BGR -> RGB)
        FE.image(frame, channels="RGB")
        FE_2.image(frame, channels="RGB")

    cap.release()