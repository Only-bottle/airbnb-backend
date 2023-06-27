from django.db import models


class House(models.Model):

    """Model Definition for Houses"""

    name = models.CharField(max_length=140)  # 길이 제한이 있는 텍스트, 단일 라인 입력
    price = models.PositiveIntegerField()  # 양의 정수
    description = models.TextField()  # 길이가 긴 텍스트, 다중 행 크기 조정 가능한 입력
    address = models.CharField(max_length=140)
