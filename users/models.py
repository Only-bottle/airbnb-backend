from django.db import models
from django.contrib.auth.models import AbstractUser


# Django가 사용하는 user를 사용 -> AbstractUser
# Django의 기본 user를 사용하지 않고 내가 만든 모델을 사용할 거라고 알려줘야 함
class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150)
    is_host = models.BooleanField()