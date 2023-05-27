from rest_framework import serializers
from ai_process.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """PictureSerializer

    Picgen view 에서 반환을 위한 시리얼라이저입니다.
    """

    class Meta:
        model = Picture
        fields = "__all__"


class PictureCreateSerializer(serializers.ModelSerializer):
    """PictureCreateSerializer

    Picgen view에서 생성을 위한 시리얼라이저입니다.
    """

    class Meta:
        model = Picture
        exclude = ("author",)
