from django.contrib import admin
from .models import House


@admin.register(House)  # admin패널에 House라는 model을 등록
class HouseAdmin(admin.ModelAdmin):
    # ModelAdmin을 그대로 상속
    pass
