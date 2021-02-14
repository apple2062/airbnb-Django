from django.urls import path
from . import views

app_name = "users"

# 아래와 같이 선언 후, config 폴더 안(core아님) urls.py에 추가해주도록 하는 거 잊지마릭
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
]
