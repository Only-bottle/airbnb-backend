from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # fieldsets과 fields 차이: 나만의 섹션을 만들 수 있음(튜플로 이루어져있음)
    # 튜플의 첫번째는 섹션의 이름, 두번째는 fields(수정하고 싶은 field 값들로 구성된 tuple)
    fieldsets = (
        (
            "Profile", 
            {
                "fields": ("avatar", "username", "password", "name", "email", "is_host", "gender", "language", "currency"),
                "classes": ("wide",),
            }
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            }
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            }
        ),
    )

    list_display = ("username", "email", "name", "is_host")
