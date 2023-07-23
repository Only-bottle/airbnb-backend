import strawberry
import strawberry.django 
from strawberry import auto
from . import models
from users.types import UserType


@strawberry.django.type(models.Review)
class ReviewType:
    id: auto
    payload: auto
    rating: auto
