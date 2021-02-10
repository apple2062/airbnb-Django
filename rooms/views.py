# RoomView 로 우린 Listview class 가 필요하기에 이를 import 해준다.
from django.views.generic import ListView, DetailView

# from django.http import Http404
# from django.urls import reverse
from django.shortcuts import render, redirect
from django_countries import countries
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
    city = request.GET.get(
        "city", "Any"
    )  # city args 없다면 Any로 반환하겠다는 소리인데, 대체할 단어는 항상 대문자로 시작해야 함!
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("geusts", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)

    # 아래 두 변수는 사용자가 선택한 체크 박스 목록들 전부를 list에 담아 반환하기 위함.(결과는 터미널에서 확인가능)
    selected_amenities = request.GET.getlist("amenities")
    selected_facilities = request.GET.getlist("facilities")
    print(selected_amenities, selected_facilities)

    # return render 할 때, 변수들이 너무 많아서 헷갈리 때는, 아래와 같이 같은 특징의 그룹끼리 나누어 표현한 뒤, 나중에 render 시 **form, **choices 와 같이 합쳐주면 편하다.
    form = {  # request 해서 받는 모든 정보는 이 form 으로감
        "city": city,
        "selected_country": country,
        "selected_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "super_host": super_host,
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {  # 데이터베이스에서 오는 것들은 전부 이 choices로 감
        "countries": countries,  # 얜 아예 모듈을 임포트한 그대로 변수로 사용 (import countries)
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(
        request,
        "rooms/search.html",
        {**form, **choices},
    )
