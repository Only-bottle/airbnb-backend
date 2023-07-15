from rest_framework import serializers

from .models import Review
from users.serializers import TinyUserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)  # 리뷰를 생성할 때, 유저가 누구인지 묻지 않기 위해

    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )