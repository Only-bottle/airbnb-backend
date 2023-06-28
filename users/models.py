from django.db import models
from django.contrib.auth.models import AbstractUser


# Django가 사용하는 user를 사용 -> AbstractUser
class User(AbstractUser):
    pass