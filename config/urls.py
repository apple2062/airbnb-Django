"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import (
    path,
    include,
)  # what include?  urls.py(in core)에 작성한 urlpatterns를 url.config에 넣어주기 위해 필요

# settings 를 import 하고 싶을때, not from . import settings! (장고는 프레임 워크라는 사실을 잊지말귕.)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ""는 / 를 의미한다
    path(
        "", include("core.urls", namespace="core")
    ),  # what include?  urls.py(in core)에 작성한 urlpatterns를 url.config에 넣어주기 위해 필요
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("admin/", admin.site.urls),
]

# static 과 URL("/media/")을 폴더(os.path.join(BASE_DIR,"uploads"))에 연결하기
if settings.DEBUG:  # ==내가 개발중이라면(프로덕션이 아니라면)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # (#8.4) static? > 장고헬퍼. static 파일들을 제공하는 것을 도움
    # /media/ 폴더를 제공하고 싶다고 static 에게 말한다. URL/media 는 media_root 안으로 들어갈 것이다.
    # 이 뒤로 사진 클릭 시, http://127.0.0.1:8000/media/room-photos/ooo.jpg를 가지게 되는 것을 확인가능
"""
# 장고에게 어떻게 폴더안의 파일들을 제공하는지 ?
# 다시말해, 내가 Amazon 같은 곳에 장고를 업로드 할 때, 어떻게 내가 파일들을 서버 폴더에 저장하지 않을 것인지 ? 를 가르쳐주겠대
# ***마지막 챕터에서 가르쳐 준대!!!!!!! 왜냐면 난 하나의 서버만을 가질 때가 있을 텐데, 그건 많은 트래픽이 발생갈 것이고 , 그래서 난 엄청 서버 코드를 복제하겠지? 그치만
# 서버 코드에서는 사용자 파일들을 저장하고 싶지 않을 거야. 그래서 Amazon s3 같은 것을 사용하는 것이고..얘는 내 파일들을 서버에 업로드 하게 해주거든
# 그래서 내가 백개의 서버를 가지던, 하개를 가지던 서버가 없건 전혀 문제 될 게 없어.
# 왜냐면 사용자가 업로드할 파일들이 Amazon s3 의 다른 저장소에 저장될테니까. 떄문에 개발할 마지막 챕터때, 작업이 이루어 질 거라 하셨다!
"""
