from django.db import models
from common.models import CommonModel


class Review(CommonModel):

    """Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,  # 유저 계정을 삭제하면 리뷰도 사라진다. (이건 개인의 차인듯? 고민해보기)
        related_name="reviews",
    )
    room = models.ForeignKey(  # review는 하나의 room만 가질 수 있다.
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",  # room은 많은 review를 가질 수 있다.
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",  # experience는 많은 review를 가질 수 있다.
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"
