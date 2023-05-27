from rest_framework import serializers
from ai_process.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """PictureSerializer

    Picgen view 시리얼라이저입니다.
    """

    class Meta:
        model = Picture
        fields = "__all__"
