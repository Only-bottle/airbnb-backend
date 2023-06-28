from django.db import models
from django.contrib.auth.models import AbstractUser


# Django가 사용하는 user를 사용 -> AbstractUser
# Django의 기본 user를 사용하지 않고 내가 만든 모델을 사용할 거라고 알려줘야 함
# 새로 추가되는 컬럼에 대해서는 default 값을 설정 잘 해줘야 함. 아니면 nullable을 하게 처리하던가
class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)  # Not Null과 Null의 중요성
