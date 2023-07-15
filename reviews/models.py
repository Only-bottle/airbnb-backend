from django.db import models
from common.models import CommonModel

# A-FK(B) -> 만약 A모델이 B모델에 대한 외래키를 가지고 있으면
# B.A_set -> B는 자동으로 A_set이라는 역접근자를 가진다. A_set은 B에게 가리키고 있는 모델 A를 준다.
# related_name으로 찾을 수 있음. room.reviews.all()

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
