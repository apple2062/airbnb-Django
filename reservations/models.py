from django.db import models
from django.utils import (
    timezone,
)  # in_progress 로 현재 숙박중인지, 아직 예정인지, 완료인지 확인할때 날짜비교를 위해 import 해주었다.
from core import models as core_models


class Reservation(core_models.TimeStampedModel):
    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CENCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CENCELED, "Canceled"),
    )

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,  # default=STATUS_PENDING
    )

    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.user", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True  # 이 놈이 패널에서 x아이콘 귀엽게 띄어줌 ㅋㅋ

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True