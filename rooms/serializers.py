from rest_framework import serializers
from .models import Amenity


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"  # 모든 field를 보여주겠다.
