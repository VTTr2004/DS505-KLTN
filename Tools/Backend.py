# input : video
# output : error of character

import pandas as pd
import numpy as np
import cv2

from Checker import Checker
from Map import Map
from Charater import Character
from Model import Model
from DeepSort import DeepSort

class BackEnd:
    
    def __inti__(self, frame, map : Map, model : Model, deepsort : DeepSort):
        self.model = model
        self.deepsort = deepsort
        self.map = map
        self.track_before = []
        self.track_now = []
        self.frame = frame
        self.index_img = 0
        self.char = dict()

    def Find_Error(self):

        df_before = pd.DataFrame(np.array(self.track_before), columns = ["Id", "Label", "X_min", "Y_min", "X_max", "Y_max"]).set_index("Id")
        df_now = pd.DataFrame(np.array(self.track_now), columns = ["Id", "Label", "X_min", "Y_min", "X_max", "Y_max"]).set_index("Id")

        for id, row in df_now.iterrows():
            if pd.notna(df_before.loc[id, "Label"]):
                box_1 = df_before.loc[id][["Label", "X_min", "Y_min", "X_max", "Y_max"]].values
                box_2 = df_now.loc[id][["Label", "X_min", "Y_min", "X_max", "Y_max"]].values
                char_temp = Character(box_1, box_2)
                self.char[id] = self.map.Check_Error(char_temp)

    def Predict(self, img):
        #

        input_deepsort = self.model.Predict()
        track_list = self.deepsort.Update(input_deepsort, self.frame)
        for track in track_list:
                id = track.track_id
                lb = track.get_det_class()
                x_1, y_1, x_2, y_2 = map(int, track.to_ltrb())

                self.track_now.append([id, lb, x_1, y_1, x_2, y_2])

        if self.index_img == 1000:
            self.map.Create_Checker(self.track_now)
            self.track_now = []
            for track in track_list:
                id = track.track_id
                lb = track.get_det_class()
                x_1, y_1, x_2, y_2 = map(int, track.to_ltrb())
                self.track_now.append([id, lb, x_1, y_1, x_2, y_2])

        elif 1001 <= self.index_img and self.index_img < 1010:
            id_list = [track[0] for track in self.track_now]
            for id in self.char:
                if id not in id_list:
                    del self.char[id]

        elif self.index_img == 1010:
            self.index_img = 1001
            self.track_before = self.track_now
            self.track_now = []
            for track in track_list:
                id = track.track_id
                lb = track.get_det_class()
                x_1, y_1, x_2, y_2 = map(int, track.to_ltrb())

                self.track_now.append([id, lb, x_1, y_1, x_2, y_2])

            self.Find_Error()

        self.index_img += 1

    def Output(self):

        for id in self.char:
            error, char = self.char.get(id)
            lb = char.Value('vehicle')
            _, x_1, y_1, x_2, y_2 = char.Value("b_2")
            color = (0, 0, 255)

            label = "{}-{}".format("-".join([i for i in lb]), id)
            cv2.rectangle(self.frame, (x_1, y_1), (x_2, y_2), color, 2)
            cv2.rectangle(self.frame, (x_1 - 1, y_1 - 20), (x_1 + len(label) * 12, y_1), color, -1)
            cv2.putText(self.frame, label, (x_1 + 5, y_1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return self.frame