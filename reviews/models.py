from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):
    """Review Model Definition"""

    review = models.TextField()
    cleanliness = models.IntegerField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )  # 유저 삭제 시, 객실 관한 정보(리뷰)도 삭제되야 하니 캐스캐이드
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )  # 객실 삭제 시, 그에 따른 리뷰들도 삭제되어야 하니 캐스캐이드

    def __str__(self):
        return f"{self.review}-{self.room}"

    def rating_average(self):  # 함수 왜 room이나 user 처럼 admin에 안쓰고 모델에 선언했냐?
        # 이는 그 모델 안에서만 보이는 기능이 아니고 전역 처럼 여기저기서 이 기능을 제공해주어야 하기 때문에 모델에 선언해주었다.
        # 그리고, 이 함수를 admin 패널에서 불러내면 됨
        # 즉, "어드민만을 위한 함수를 만들고 싶은데, 그 기능을 모든 곳에 포함하고 싶다면 그 함수는 model에 넣을 수 있다"
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "AVG."