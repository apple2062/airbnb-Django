# 이게 있음으로서 HttpResponse(content="<h1> Hi! </h1>") 같이 html 형식으로 서버에 보내는 rendering 이 가능
from django.shortcuts import render
from . import models

# from djangi.http import HttpResponse


def all_rooms(request):
    all_rooms = models.Room.objects.all()
    # render 의 인자를 살펴보면, request 가 필요함.
    # request 없이 response 는 있을 수 없음. 그래서 뭔가를 render 하고 싶다면, request를 주어야 함.(render(request, ... ))
    return render(
        request, "rooms/home.html", context={"rooms": all_rooms}
    )  # context 에 지정한 변수명과 변수를 담아 해당 template으로 전달
    # template 에서는 받을 변수를 {{}} 안에 호출시킨다.

    # return HttpResponse(content = "hello~")
