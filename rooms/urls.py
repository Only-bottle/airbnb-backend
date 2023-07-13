from django.urls import path

from .views import Rooms, Amenities, AmenityDetail


urlpatterns = [
    path("", Rooms.as_view()),
    path("amenities/", Amenities.as_view()),
    path("amenities/<int:pk>", AmenityDetail.as_view()),
]
