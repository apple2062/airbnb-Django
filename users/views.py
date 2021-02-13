from django.shortcuts import render
from django.views import View
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        print(form)
        # 위와 같이 form 을 프린트 해보면, 나의 웹사이트에서 보내진 post request임을 확인하고, 맞기 때문에 그에 대한 정보(email, password) 정보를 콘솔에 출력해준다.
        # 관련된 노트는 #14.1 과 login.html 의 <csrf_token> 함께 보자
