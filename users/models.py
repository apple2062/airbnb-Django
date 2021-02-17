# from django.db import models  # 우리한테 필요없는 모델
from django.contrib.auth.models import AbstractUser  # 우리가 쓸 모델
from django.db import models

# (#8.6)의 rooms를 useradmin 안에 Inline 해보라는 과제 때문에 import 시켜준 room model이다.
from rooms import models as room_models

# 장고 user을 내가 만든 user 대치하기 -> 이때, 가장 먼저 할일 : User 어플리케이션을 setting.py 에서 설치해야함
class User(AbstractUser):
    # 이 AbstractUser 을 넣음으로써, 0001_initail.py 에 있는 필드들을 기본적으로 가지게 됨

    """ Custom User Model"""  # << 클래스를 만들 때마다 넣는 파이썬에서 쓰는 표준 문구 형식. 이게 무슨 클래스인지 설명해주는 것.
    # 위 docstring 이 잘 작동하는지 확인하려면 admin.py에 가서 models.User 의 User 부분에 마우스 갖다대보라.

    GENDER_MALE = "male"  # constant 생성
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),  # (db 로 가는 값, admin 패널 form 에서 보여지는 값)
        (LANGUAGE_KOREAN, "Korea"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KR = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KR, "KRW"),
    )

    photo = models.ImageField(
        upload_to="avatar-photos", blank=True
    )  # upload-to? 장고야,uploads 폴더 안의 avatar-photos라는 폴더에 업로드 해줘!(폴더가 없다면 너가 자동 생성해!)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )  # charfeild 는 내가 약간 변형가능(like choices)
    bio = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KR
    )
    superhost = models.BooleanField(default=False)