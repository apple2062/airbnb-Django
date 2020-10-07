from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models  # 현재 같은 폴더 내에 있는 models 파일을 import 하겠다는 뜻.


# Register your models here.
@admin.register(models.User)  # == admin.site.register(models.User,CustomUserAdmin)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "photo",
                    "gender",
                    "bio",
                    "birthday",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )