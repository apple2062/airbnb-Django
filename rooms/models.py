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
    file = models.ImageField(
        upload_to="room-photos"  # upload_to? 장고야, uploads 폴더 안의 room-photos 폴더에 사진을 업로드 해줘!(폴더 없으면 너가 생성해!)
    )  # room 은 photo 와 연결이 되어야 하므로 이를 연결시켜줌 (그리고 room 은 user 와 연결됨)
    room = models.ForeignKey(
        "Room", related_name="photos", on_delete=models.CASCADE
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
        related_name="rooms",  # (= user가 어떻게 우리를 찾기를 원합니까?) room__set 대신 room 이라 쳐서 찾길 원해! >> 터미널에서, 변수.room.all()으로 검색할수 있게됨!
        # 결국, "room" 이 set 이 된 것 이다!
        on_delete=models.CASCADE,  # host 필드가 user 과 연결이 되있는 결과를 확인할 수 있음!
    )  # host 는 결국 user 인 셈이기 떄문에, user 모델과 이 모델을 연결해서 쓰면 되는 것임. so, import user
    # cascade 는 내가 user 을 삭제했을 때, room 도 삭제하고자 하기 위함이다.
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True
    )  # Manytomany 는 다대다 관계
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rule = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)  # 사용자가 소문자로 입력시 첫 글자 대문자로 바꿔주기 위함
        super().save()

    def total_rating(self):  # room 에서 review 의 모든 리뷰들을 가져와서 평균을 얻기 위한 함수.
        # 이 함수도 왜 admin에 안쓰고 model에 써준거냐? reviwq 패널 외의 다른 곳에도 그 평균 제공 기능이 존재하기때문
        all_reviews = (
            self.reviews.all()
        )  # class Riview 가보면, room 을 가지고 있음. 그리고 그 룸은 related_name= "reviews"를가짐
        # 그 말은, room 이 reviews 를 가진다는 것

        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0