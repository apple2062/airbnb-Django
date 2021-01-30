# RoomView 로 우린 Listview class 가 필요하기에 이를 import 해준다.
from django.views.generic import ListView
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

    def def get_context_data(self, **kwargs):
        context = super(ViewName, self).get_context_data(**kwargs)
        return context
