from django.db import models
from core import models as core_models


class List(core_models.TimeStampedModel):
    """List Model Definition"""

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rooms = models.ManyToManyField(
        "rooms.room", blank=True
    )  # list 하나는 여러개의 room 을 가질 수 있음

    def __str__(self):  # 후에 이 안에 객실을 개수를 넣어줄것임
        return self.name