from rest_framework import serializers

from .models import Room, Amenity


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"  # 모든 field를 보여주겠다.
