# detail.html 을 위해 생성한 파일.
# detail.html 은 core 내의 url 이 필요 없기에 ,room 앱 안에서 url을 만들어 주었다.

from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path(  # 이 path도 선언 후 config 안의 url파일 내에 import 해주어야만 한다.
        "<int:pk>", views.RoomDetail, name="detail"
    )
]
