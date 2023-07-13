from django.urls import path

from .views import Rooms, RoomDetail, Amenities, AmenityDetail


urlpatterns = [
    path("", Rooms.as_view()),
    path("<int:pk>", RoomDetail.as_view()),
    path("amenities/", Amenities.as_view()),
    path("amenities/<int:pk>", AmenityDetail.as_view()),
]
