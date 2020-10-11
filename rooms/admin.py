from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = (
        "name",
        "used_count",
    )

    def used_count(
        self, obj
    ):  # self = ItemAdmin, obj = models.RoomType(or Facility, Amemity, HouseRule..)
        return (
            obj.rooms.count()
        )  # amenities, facilities, roomtype, houserule class 확인시 related_name = "rooms"로 해놓았음


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 패널을 접었다가 펼쳤다 할 수 있는 기능
                "fields": ("amenities", "facilities", "house_rule"),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",  # 그냥 amenities를 쓰지 못하는 이유: 이 놈은 ManyToMany 필드 이기 때문에 한 놈만 display 할 수 없음. 따라서 새로운 함수를 만들어서 그에 따라 amaenity개수를 보여주고자 함.
        # 이 때, 새로운 함수는 admin functions 으로 같은 admin 안에서 생성할 수 있고, 내가 원하는 이름을 지으면 됨
        "count_photos",  # 얘도 마찬가지고 ManytoMany 필드이기 때문에, 새로운 함수를 만들어서 photo개수를 보여주고자 함.
    )

    ordering = (
        "name",
        "price",
        "bedrooms",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rule",
        "city",
        "country",
    )
    search_fields = (
        "=city",
        "^host__username",  # host 는 room model 에 있고, host의 foreinkey 인 user 가 가진 username 을 검색. 그리고 search_field에선 . 아니고 __
    )  # 검색 시, city 에 해당 내용이 있는지없는지를 판단해서 show. 검색결과 아무것도 찾아내지 못했다면 호스트 username 으로 검색

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rule",
    )

    def count_amenities(
        self, obj
    ):  # self 는 adminclass 즉, 현재 포함되어 있는 RoomAdmin 이고 두번째 인자는 object 를 받는데 object 는 '현재 Room(class)' 이다.
        return obj.amenities.count()

    count_amenities.short_description = (
        "how many amenity"  # panel 에 뜨는 문구를 COUNT_AMENITY 대신 이 문구로 뜨게 함.
    )

    def count_photos(self, obj):  # obj = (class)Room , self = 현재 포함된 RoomAdmin을 뜻함ㄴ
        return (
            obj.photos.count()
        )  # photos -> model 에서 class Photo가 related_name 으로 photos 를 갖고 있음


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ """

    pass
