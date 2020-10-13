from django.contrib import admin
from django.utils.html import mark_safe
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


class PhotoInline(admin.TabularInline):  # Rooms 안에 administration of photos 를 가지기 위한 작업
    # InlineModelAdmin? > admin안에 또다른 admin을 넣는 방법(docs 참고!)
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    inlines = [
        PhotoInline,  # 바로 윗 줄의 inline 인 PhotoInline을 RoomAdmin에 포함시켜주는 작업 (활용방법은 docs 참조 )
    ]  # inline 포함 후, rooms 패널 가보면 장고가 자동으로 room 의 FK를 가지고 있는 이미지(PHOTOS) 를 집어 넣는다.

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
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
        "total_rating",
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

    raw_id_fields = (
        "host",
    )  # user가 엄~~청 많다면, host를 선택하는 작업에서 엄청나게 많은 이용자중에 찾아야 하는 무식함이 발생하기에,
    # 많은 유저가 있을 것을 대비 , 이 raw_id 를 사용하여 필터(?) 작업을 해주는 것임

    search_fields = (
        "=city",
        "^host__username",  # host 는 room model 에 있고, host의 foreinkey 인 user 가 가진 username 을 검색. 그리고 search_field에선 . 아니고 __
    )  # 검색 시, city 에 해당 내용이 있는지없는지를 판단해서 show. 검색결과 아무것도 찾아내지 못했다면 호스트 username 으로 검색

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rule",
    )

    # model 에서는 save(), admin에서는 save_model()을 씀
    def save_model(self, request, obj, form, change):
        # obj.user = request.user
        print(
            obj, change, form
        )  # obj = Yeonju room , change 는 바뀌었는지 아닌지 True or False 를 보여줌
        super().save_model(request, obj, form, change)

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
    """Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(
        self, obj
    ):  # 사용자에게 썸네일을 어드민 패널에서 보여주기 위함. 패널에서만 쓸 것이라 얜 model 아닌 admin 에 만들어주엇다.
        return mark_safe(f'<img width="30px" src="{obj.file.url}" />')
        # mark_safe? 내가 직접 html 을 만들어 쓰는 것을 시도하였더니, 장고가 access해주지 않아. 그것은 장고가 알 수없는 html로부터 hacked 되는 것을
        # 막기 위해 일부러 액세스 안해주는 것. 때문에 나는 장고에게 이게 정말 안전하단 뜻으로 mark_safe utility를 import 해준 뒤, 그를 이렇게 활용한다

    get_thumbnail.short_description = "Thumbnail"