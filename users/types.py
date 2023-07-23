import strawberry
import strawberry.django 
from strawberry import auto
from . import models


@strawberry.django.type(models.User)
class UserType:
    name: auto
    email: auto
    username: auto
