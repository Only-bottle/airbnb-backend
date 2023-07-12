from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    # ModelSerializer - 자동으로 model의 field를 파악한다.

    class Meta:
        model = Category
        fields = "__all__"  # 모든 field를 보여주겠다.
        # fields = ("name", "kind")  # 직접 어떤 걸 보여줄 것인지 선택
        # exclude = ("created_at")  # 제외시킬 값 선택