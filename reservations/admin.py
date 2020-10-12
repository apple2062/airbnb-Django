from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin Definition"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)  # "in_progress")
    # 우리가 생성한 것(함수)들을(in_progress, is_finished) 가지고 필터 할 수 있다면 얼마나 좋을까..?
    #