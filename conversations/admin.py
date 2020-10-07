from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.models):
    """List Admin Definition"""

    pass
