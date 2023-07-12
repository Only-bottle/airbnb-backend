from django.urls import path
from . import views


urlpatterns = [
    path("", views.Categories.as_view()),  # as_view는 요청에 따라 class에 구현한 method가 실행됨
    path("<int:pk>", views.CategoryDetail.as_view()),
]
