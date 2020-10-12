from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin Definition  """

    list_display = (
        "__str__",
        "rating_average",
    )  # 이와 같은 식으로 나의 __str__을 list_display에 쓸 수 있음
