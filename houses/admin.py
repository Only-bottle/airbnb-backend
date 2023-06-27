from django.contrib import admin
from .models import House


@admin.register(House)  # admin패널에 House라는 model을 등록
class HouseAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "address",
        ("price_per_night", "pets_allowed")
    )  # admin 패널에서 보고 싶은 field들을 의미. 여러 개의 field를 같은 줄에 보이게 하려면 tuple로 묶으면 된다.
    list_display = (
        "name",
        "price_per_night",
        "address",
        "pets_allowed",
    )  # 리스트의 컬럼들을 보여줌.
    list_filter = ("price_per_night", "pets_allowed")
    search_fields = ("address",)  # address__startswith: 입력하는 텍스트로 시작하는 것만 검색
    list_display_links = ("name", "address")  # 리스트 내에서 링크로 지정할 필드 목록 (이를 지정하지 않으면, 첫번째 필드에만 링크가 적용)
    list_editable = ("pets_allowed",)  # 목록 상에서 수정할 필드 목록