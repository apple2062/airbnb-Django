from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):
    """Review Model Definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )  # 유저 삭제 시, 객실 관한 정보(리뷰)도 삭제되야 하니 캐스캐이드
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE
    )  # 객실 삭제 시, 그에 따른 리뷰들도 삭제되어야 하니 캐슼캐이드

    def __str__(self):
        return f"{self.review}-{self.room}"
