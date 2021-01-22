from math import ceil

# render가 있음으로서 HttpResponse(content="<h1> Hi! </h1>") 같이 html 형식으로 서버에 보내는 rendering 이 가능
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

# from djangi.http import HttpResponse


def all_rooms(request):
    page = request.GET.get(
        "page", 1
    )  # url 에서 온 page 가 문자열이고 내가 1로 설정한 default 는 숫자이므로 에러 방지위해 int형변환을 해주는것임
    page = int(  # url 에서 온 page 가 문자열이고 내가 1로 설정한 default 는 숫자이므로 에러 방지위해 int형변환을 해주는것임
        page or 1
    )  # 이미 위에서 1로 페이지가 생성됐다면, 다시 빈페이지로 page 입력 시, 에러나 나기 떄문에 이를 방지 하기 위함
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    # render 의 인자를 살펴보면, request 가 필요함.
    # request 없이 response 는 있을 수 없음. 그래서 뭔가를 render 하고 싶다면, request를 주어야 함.(render(request, ... ))
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page_num": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )  # context 에 지정한 변수명과 변수를 담아 해당 template으로 전달
    # template 에서는 받을 변수를 {{}} 안에 호출시킨다.

    # return HttpResponse(content = "hello~")
