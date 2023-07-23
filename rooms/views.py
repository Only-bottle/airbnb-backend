from django.db import transaction
from django.conf import settings
from django.utils import timezone  # djangodㅔ서 시간을 알아내거나 타임존에 관한 작업을 하려면 해당 라이브러리를 쓰는 게 좋음
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Room, Amenity
from .serializers import RoomListSerializer, RoomDetailSerializer, AmenitySerializer
from categories.models import Category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            # category는 create함수에 전달되지 않는다 -> read_only로 설정했기 떄문에
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():  # db에 즉시 반영하지 않는다. 에러가 발생하지 않으면 db에 반영
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )  # 해당 serializer의 create 함수에 validated_data가 추가된다.
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        # 잘못된 Amenity를 보낸 경우 어떻게 처리해야 할까
                        # 1. 조용히 실패 pass 같은 방식
                        # 2. 에러 메시지를 띄우고 room을 지워버리기
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)  # ManyToMany이기 때문에 foreign key와는 다르다.
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found")
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},  # 내가 원하는 어떤 데이터를 serializer에게 넘겨줄 수 있음
        )
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)

        if room.owner != request.user:  # 방 주인이 같은지 확인
            raise PermissionDenied

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")

            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        room = serializer.save(category=category)
                    else:
                        room = serializer.save()

                    amenities = request.data.get("amenities")
                    if amenities:
                        # all().delete()와의 차이 알아두기
                        room.amenities.clear()  # Removes all objects from the related object set
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)

                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)

            except Exception:
                raise ParseError("Amenity not found")

        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:  # 방 주인이 같은지 확인
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)  # 기본값은 1
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE

        start = (page - 1) * page_size  # page=1이면, start 0
        end = start + page_size  # 0 + 3 = 3

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],  # 모든 리뷰를 불러와서 슬라이싱을 하는 거처럼 보이지만 그렇지 않음. Limiting QuerySets 참고
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)  # 기본값은 1
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE

        start = (page - 1) * page_size  # page=1이면, start 0
        end = start + page_size  # 0 + 3 = 3

        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],  # 모든 리뷰를 불러와서 슬라이싱을 하는 거처럼 보이지만 그렇지 않음. Limiting QuerySets 참고
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)  # 사진이 속한 방의 정보도 같이 넘겨줘야 함.
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()  # check_in 날짜가 미래인 booking을 가져와야 함
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
