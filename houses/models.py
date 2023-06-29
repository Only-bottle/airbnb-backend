from django.db import models


class House(models.Model):

    """Model Definition for Houses"""

    name = models.CharField(max_length=140)  # 길이 제한이 있는 텍스트, 단일 라인 입력
    price_per_night = models.PositiveIntegerField(
        verbose_name="Price", 
        help_text="Positive Numbers Only"
    )  # 양의 정수
    description = models.TextField()  # 길이가 긴 텍스트, 다중 행 크기 조정 가능한 입력
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(
        verbose_name="Pets Allowed?",  # 사람이 읽을 수 있는 이름을 field에 부여, default는 attribute 이름
        default=True,
        help_text="Does this house allow pets?"
    )  # True, False
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE  # ForeignKeyField가 바라보는 값이 삭제될 때 해당 요소를 처리하는 방법을 지정. 모델 인스턴스를 같이 삭제시킨다.
    )

    def __str__(self) -> str:
        return self.name