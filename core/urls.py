"""
프로젝트를 하다보면 엄청난 양의 url 이 발생하기때문에 이를 위해 divide and conquer 이 필요하다
다시말해, /rooms 로 시작하는 url 들은 room 파일로 가게하고,
/users 로 시작한다면 그것은 user 파일로 가게하는데,
아무것으로도 시작하지않는, 예를 들면 /home, /login, /logout 같은 것들은 바로 여기, core 로 가게 한다.
장고안의 어플리케이션들은 기본으로 urls.py(in config) 로 오지 않는다. 만들어야됨..!
"""
from django.urls import path
from rooms import views as room_views

app_name = "core"  # 지금 이 앱 네임인 core 와 config 안의 urls.py 의 namespace 랑 이름이 깉아야한다.

urlpatterns = [
    path(
        "", room_views.all_rooms, name="home"  # view 에 home 이라는 이름을 주었음
    ),  # 이렇게 하고, urls.py(in config) 가서 path를 include 해주는 작업만 해주면 된다.
]