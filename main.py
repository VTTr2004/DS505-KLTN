import streamlit as st
import tempfile
import cv2
import os
import time

from ultralytics import YOLO

# from Tools.Backend import BackEnd
# from Tools.FrontEnd import FrontEnd

from Tools.Process_OutPut import ProOP
from Tools.Charater import Character
from Tools.Checker import Checker
from Tools.Map import Map
from worker.drawer import Draw



# contants

model = YOLO('./Tools/final.pt')
conv_OP = ProOP()
charer = Character()
checker = Checker()
mapper = Map(128, 128, charer, checker)
drawer = Draw() 

# frame = cv2.imread('./Tools/img_1.jpg')
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# result = model(frame)
# result = conv_OP.OutForMap(frame, result[0])
# mapper.UpdateData(result, 10)
# result = mapper.GetListChar()
# frame = drawer.DrawFromMap(frame, result)

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
        result = model(frame)
        # result = conv_OP.OutForMap(frame, result[0])
        # mapper.UpdateData(result, 10)
        # result = mapper.GetListChar()
        # frame = drawer.DrawFromMap(frame, result)
        # FE.image(frame, channels="RGB")

        frame = drawer.DrawFromModel(frame, result)
        FE.image(frame, channels="RGB")

        # FE_2.image(frame, channels="RGB")

        time.sleep(1 / 5)

    cap.release()


