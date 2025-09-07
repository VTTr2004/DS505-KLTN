# from django.db import models

# class CamInfor(models):
#     cam_id = models.CharField(max_length=10)
#     cam_name = models.TextField()
#     street_name = models.TextField()
#     cam_path = models.TextField()
#     def __str__(self):
#         return f"{self.cam_name}"
    
# class CamDetail(models):
#     detail_id = models.CharField(max_length=10)
#     cam_id = models.CharField(max_length=10)
#     date = models.DateField()
#     video_path = models.TextField()

# class ViolationTraffic(models):
#     x = models.IntegerField()
#     y = models.IntegerField()
#     w = models.IntegerField()
#     h = models.IntegerField()
#     detail_id = models.CharField(max_length=10)
#     id_frame = models.IntegerField()
#     def __str__(self):
#         return f"{self.detail_id} - {self.id_frame}"