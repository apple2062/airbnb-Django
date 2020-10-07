from django.db import models

# core 가 뭐냐? 한 application 안에 쓰이는 기능?이 다른 application에서도 많이 쓰일 때,
# 전역변수 처럼 활용하기 위한 "다른 app이 재사용이 가능한 common file".


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(
        auto_now_add=True
    )  # 장고가 내가 새로운 모델을 만들면 현재 날짜와 시간을 이 안에 넣어주는 속성(=모델이 생성된 날짜)
    updated = models.DateTimeField(
        auto_now=True
    )  # 내가 모델을 저장할 때마다 항상 새로운 날짜를 써주는 속성(=새로운 날짜로 업데이트)

    class Meta:  # 기타 사항
        abstract = True  # abstract란 모델은 모델이나, db 에 나타나지 않는 모델 즉 대부분의 abstract 모델은 확장을 하려고 사용. 이걸 설정안해주면 db에 이 모델이 등록되어버림.
