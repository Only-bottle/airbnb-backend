from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"  # 필터의 이름

    parameter_name = "word"  # 필터에 사용될 컬럼의 이름(데이터베이스상에서 존재하는 이름이여야함)

    def lookups(self, request, model_admin):  # 필터 창에서 보이게되는 것을 구현한 메소드
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):  # 필터 창에서 특정 필터를 선택(클릭)했을때의 동작방법을 구현한 메소드
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class ScoreFilter(admin.SimpleListFilter):

    title = "Filter by scores!"

    parameter_name = "score"

    def lookups(self, request, model_admin):
        return [
            ("bad", "Bad"),
            ("good", "Good")
        ]

    def queryset(self, request, reviews):
        score = self.value()

        if score == "bad":
            return reviews.filter(rating__lt=3)
        elif score == "good":
            return reviews.filter(rating__gte=3)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        ScoreFilter,
        "rating",
        "user__is_host",  # foreign key로 필터링이 가능!
        "room__category",
        "room__pet_friendly",
    )
