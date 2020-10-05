from django.db import models  # 우리한테 필요없는 모델
from django.contrib.auth.models import AbstractUser  # 우리가 쓸 모델

# Create your models here.

# 장고 user을 내가 만든 user 대치하기 -> 이때, 가장 먼저 할일 : User 어플리케이션을 setting.py 에서 설치해야함
class User(AbstractUser):
    # 이 AbstractUser 을 넣음으로써, 0001_initail.py 에 있는 필드들을 기본적으로 가지게 됨

    pass
