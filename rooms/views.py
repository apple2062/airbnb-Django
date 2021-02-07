# RoomView 로 우린 Listview class 가 필요하기에 이를 import 해준다.
from django.views.generic import ListView, DetailView

# from django.http import Http404
# from django.urls import reverse
 from django.shortcuts import render, redirect
from . import models

# 11.6 까지 했던 모든 paginator 와 try-except 로 예외 처리했던 모든 부분을 지우고 아래와같이 Homeview라 선언한 class based view로 다시 시작해보자.
# 추가적으로 core 폴더의 urls.py 내 urlpatterns 도 바뀐 것에 맞게 room_views.HomeView 로  수정해주어야 겠지.
class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    # 아래와 같이 작성하면서, room_list.html에서는 object_list 대신 rooms라 써서 object 불러옴
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """ RoomDetail Definition """

    model = models.Room


"""
def room_detail(request, pk):  # urls 에서 내가 선언한 pk 변수를 인자로 받아서 쓰면 됨
    try:
        # db 에서 room 정보 갖고 오기
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))  # core:home url을 받아서 redirect 해줄 것임
        # reverse를 url 대신 쓸 수 있도록 연습하자! 엄청 도움이 된다고 한다
        raise Http404()
"""

def search(request):
    return render(request, "")
