from django.db import models
from django_countries.fields import CountryField
from core import models as core_models
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):  # RoomType 을 만들기위해 생성한 class
    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]


class Amenity(AbstractItem):
    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(
    core_models.TimeStampedModel
):  # 아래 코드 중, Foreign 키로 Room이 연결되어 줘야 하므로 위에있으면 파이썬이 Room 을 못찾음. Room class 아래에 이 photo클래스 선언해주어야함.
    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = (
        models.ImageField()
    )  # room 은 photo 와 연결이 되어야 하므로 이를 연결시켜줌 (그리고 room 은 user 와 연결됨)
    room = models.ForeignKey(
        "Room", on_delete=models.CASCADE
    )  # 사진을 지우면 room도 연결되어있기 떄문에 함께 지워져야 함

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140, blank=True)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,  # host 필드가 user 과 연결이 되있는 결과를 확인할 수 있음!
    )  # host 는 결국 user 인 셈이기 떄문에m, user 모델과 이 모델을 연결해서 쓰면 되는 것임. so, import user
    # cascade 는 내가 user 을 삭제했을 때, room 도 삭제하고자 하기 위함이다.
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", blank=True)  # Manytomany 는 다대다 관계
    facilities = models.ManyToManyField("Facility", blank=True)
    house_rule = models.ManyToManyField("HouseRule", blank=True)

    def __str__(self):
        return self.name
