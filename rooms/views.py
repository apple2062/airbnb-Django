# RoomView 로 우린 Listview class 가 필요하기에 이를 import 해준다.
from django.views.generic import ListView, DetailView

# from django.http import Http404
# from django.urls import reverse
from django.shortcuts import render, redirect
from django_countries import countries
from . import models, forms

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

    form = forms.SearchForm(request.GET)

    if form.is_valid():

        city = form.cleaned_data.get("city")
        country = form.cleaned_data.get("country")
        price = form.cleaned_data.get("price")
        room_type = form.cleaned_data.get("room_type")
        price = form.cleaned_data.get("price")
        guests = form.cleaned_data.get("guests")
        bedrooms = form.cleaned_data.get("bedrooms")
        beds = form.cleaned_data.get("beds")
        baths = form.cleaned_data.get("baths")
        instant_book = form.cleaned_data.get("instant_book")
        superhost = form.cleaned_data.get("superhost")
        amenities = form.cleaned_data.get("amenities")
        facilities = form.cleaned_data.get("facilities")

        filter_args = {}
        # city__startswith 의 city 는 models.py 안에서 내가 선언한 변수명을 똑같이 쓴 것. 아래의 조건부도 동일한 방법으로 써야함.
        if city != "Any":
            filter_args["city__startswith"] = city

        # country 는 default 를 KR 로 해놓았기 때문에, 조건부를 설정할 필요가 없이 그냥 fileter_args에 집어넣어주면 됨.
        filter_args["country"] = country

        if room_type is not None:
            filter_args["room_type"] = room_type

        if price is not None:
            filter_args[
                "price__lte"
            ] = price  # price 는 사용자 입장에서 하루 최대 숙박비이므로 __lte 를 활용

        if guests is not None:
            filter_args[
                "guests__gte"
            ] = guests  # geust 같은 경우는 가장 최소 인원으로 선택하게 되니깐 __gte 를 활용

        if bedrooms is not None:
            filter_args["bedrooms__lte"] = bedrooms

        if beds is not None:
            filter_args["beds__lte"] = beds

        if baths is not None:
            filter_args["baths__lte"] = baths

        # instant_book 은 models.py에서 선언했던 변수명으로서 가져온 것임
        if instant_book is not True:
            filter_args["instant_book"] = True  # False 인건 신경 안써도 되니까 그냥 조건부없이 True 해줌

        # super_host 는 models.py 안에 있지 않아. 그러나 FK 를 이용해서 필터링이 가능하다 !!!
        if superhost is not True:
            # host 는 models.py를 보면, host 의 FK가 user이고 user 내부모델에 superhost 가 있으므로 이런식으로 필터링을 한다는 것임
            filter_args["host__superhost"] = True

        for amenity in amenities:
            filter_args["amenities"] = amenity

        for facility in facilities:
            filter_args["facilities"] = facility

        rooms = models.Room.objects.filter(**filter_args)

    else:
        form = forms.SearchForm()

    return render(
        request,
        "rooms/search.html",
        {"form": form, "rooms": rooms},
    )