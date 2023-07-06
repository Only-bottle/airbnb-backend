from django.db import models
from common.models import CommonModel


class Room(CommonModel):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(max_length=180, default="")
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )  # 여러 개의 amenity를 가질 수 있음
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rooms",
    )

    def __str__(self) -> str:
        return self.name

    # admin 패널에서도 메소드를 넣을 수도 있음. admin 패널만을 위한 것이 아니라면 model에 구현하는 게 좋음
    def total_amenities(self):
        return self.amenities.count()
    
    def rating(self):
        count = self.reviews.count()
        if count == 0:
            return "No Reviews"
        else:
            total_rating = 0
            for review in self.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)

class Amenity(CommonModel):
    """Amenity Model Definition"""

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"
