from django.db import models


class CommonModel(models.Model):

    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)  # 필드 값을 해당 object가 처음 생성되었을 때의 date로 설정
    updated_at = models.DateTimeField(auto_now=True)  # object가 저장될 때마다 현재 date로 설정

    class Meta:  # 
        abstract = True  # 해당 모델을 DB에 저장하지 않게 함. 다른 APP에서 재사용하게 하기 위함
