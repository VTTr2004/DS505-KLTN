from deep_sort_realtime.deepsort_tracker import DeepSort

class Track_Tool:
    def __init__(self, max_age, class_name = None,threshold = 0.5, tracking_class = None):
        self.model = DeepSort(max_age = max_age)
        self.tracks = []
        self.class_name = class_name
        self.threshold = threshold
        self.tracking_class = tracking_class

    def Update(self, ip_deepsort, frame):
        # tracking and return track_list

        self.tracks = self.model.update_tracks(ip_deepsort, frame = frame)

        return self.tracks

    def Get_TrackClass(self):
        # return track_class

        return self.tracking_class
