# from django.db import models  # 우리한테 필요없는 모델
from django.contrib.auth.models import AbstractUser  # 우리가 쓸 모델
from django.db import models

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

    photo = models.ImageField(blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )  # charfeild 는 내가 약간 변형가능(like choices)
    bio = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    superhost = models.BooleanField(default=False)