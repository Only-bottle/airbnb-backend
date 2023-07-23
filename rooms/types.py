import strawberry
import strawberry.django 
from strawberry import auto
from . import models


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
