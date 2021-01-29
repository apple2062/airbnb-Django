from math import ceil

# render가 있음으로서 HttpResponse(content="<h1> Hi! </h1>") 같이 html 형식으로 서버에 보내는 rendering 이 가능
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models

# from djangi.http import HttpResponse


def all_rooms(request):
    page = request.GET.get("page", 1)  # Paginator 가 알아서 해주므로 dafault값 설정할 필요가 없어짐.
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)  # orphan에 관한건 11.5 필기참고
    try:
        # .page는 인자가 int 형아니면 에러남. get_page 와 page의 차이는 11.4 필기 참조
        rooms = paginator.page(int(page))
        # print(vars(rooms.paginator)) 해보면 Queryset 안에 count, num_pages, per_page등 수많은 기능(?) 이 존재함을 볼 수 있다.
        # render 의 인자를 살펴보면, request 가 필요한데, request 없이 response 는 있을 수 없음. 그래서 뭔가를 render 하고 싶다면, request를 주어야 함.(render(request, ... ))
        return render(request, "rooms/home.html", {"rooms": rooms})
    except EmptyPage:  # emptypage 는 import 해주어야함
        return redirect("/")

    # return HttpResponse(content = "hi~")
