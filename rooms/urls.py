from django.urls import path

from .views import Rooms, RoomDetail, RoomReviews, RoomPhotos, RoomBookings, RoomAmenities, Amenities, AmenityDetail, RoomBookingCheck


urlpatterns = [
    path("", Rooms.as_view()),
    path("<int:pk>", RoomDetail.as_view()),
    path("<int:pk>/reviews", RoomReviews.as_view()),
    path("<int:pk>/amenities", RoomAmenities.as_view()),
    path("<int:pk>/photos", RoomPhotos.as_view()),
    path("<int:pk>/bookings", RoomBookings.as_view()),
    path("<int:pk>/bookings/check", RoomBookingCheck.as_view()),
    path("amenities/", Amenities.as_view()),
    path("amenities/<int:pk>", AmenityDetail.as_view()),
]
