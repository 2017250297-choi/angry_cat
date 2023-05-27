from django.db import models


class Picture(models.Model):
    """Picture 모델

    Picgen view가 발생할때마다 입력사진과 변환사진을 저장합니다.

    Attributes:
        input_pic (Image): 입력된 사진
        change_pic (Image): AI가 변환한 사진
    """

    input_pic = models.ImageField(upload_to="temp/%Y/%m/input/")
    change_pic = models.ImageField(upload_to="temp/%Y/%m/change/", null=True)
