from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(  # 많은 사진들을 한 개의 방에 종속시킬 수 있음
        "rooms.Room",
        on_delete=models.CASCADE,  # 방이 삭제되면 사진도 삭제되어야 함
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):

    file = models.URLField()  # 파일을 클라우드에 올리고 파일의 URL을 저장하기 위함.
    experience = models.OneToOneField(  # ForeignKey와 같지만 고유한 값이 된다. (하나의 활동엔 하나의 비디오)
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="videos",
    )

    def __str__(self):
        return "Video File"
