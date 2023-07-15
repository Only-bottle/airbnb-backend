from rest_framework import serializers

from .models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)  # 읽기만 해야하는 필드
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()
    # 연결되어 있는 serializer 클래스에서 메소드를 호출하여 값을 가져올 수 있는 읽기 전용 필드이다.
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]  # view에서 전달한 context를 확인
        return room.owner == request.user


class RoomListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
