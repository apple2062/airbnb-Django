from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models  # 현재 같은 폴더 내에 있는 models 파일을 import 하겠다는 뜻.


class RoomInline(admin.TabularInline):
    model = models.room_models.Room


# Register your models here.
@admin.register(models.User)  # == admin.site.register(models.User,CustomUserAdmin)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin """

    inlines = [
        RoomInline,
    ]

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

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )