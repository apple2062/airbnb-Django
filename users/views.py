from django.shortcuts import render, redirect, reverse

# reverse_lazy ? reverse 와 기능은 동일하나, 자동으로 호출 하지 않는 것. View가 필요로 할 때 호출
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    # form_valid ? (특징에 대한 것 #14.5 꼭 참고) 말 그대로 form 이 유효한지 체크. 그에 따라 어디론가 보내줄 필요도, 다른 걸 할 필요도 없음.
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        # super().form_valid() 호출될때, success_url 로 가고 다 다시 작동되게 됨
        return super().form_valid(form)


def log_out(request):
    # 아래 logout은 위에서 import logout 해준 것임
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "lee",
        "last_name": "yeonju",
        "email": "yamjuzzang@gmail.com",
    }

    def form_valid(self, form):
        form.save()
        # forms.py 내의 ModelForm (in SignupForm) 이 save 기능을 갖고 있기 때문에 이전 코드 삭제.
        return super().form_valid(form)
