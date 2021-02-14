from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "yeonju@lee.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # 로그인 하기 위한 두가지 방법 : 인증 과 로그인. (#14.4)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


def log_out(request):
    # 아래 logout은 위에서 import logout 해준 것임
    logout(request)
    return redirect(reverse("core:home"))