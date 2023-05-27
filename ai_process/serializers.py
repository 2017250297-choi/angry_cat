from rest_framework import serializers
from ai_process.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """PictureSerializer

    Picgen view 에서 반환을 위한 시리얼라이저입니다.
    """

    class Meta:
        model = Picture
        fields = "__all__"
        extra_kwargs = {"author": {"read_only": True}}
