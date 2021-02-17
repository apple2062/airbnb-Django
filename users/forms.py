from django import forms
from . import models

# 내가 이 폼 안에서 할 것 은 모든 로그인과 회원가입을 Django 안에서 username == email 이도록 설정할 것임
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(
                email=email  # 나중에 모든 계정에 대한 username과 email이 같에 할거지만, 지금 내가 만든 admin은 username과 email이 서로 달라 에러나므로 잠시 email=email로 변경
            )  # check_password 메소드 ? 패스워드를 확인하기 위해서는 user의 정보가 필요할 것이다. 때문에 이 메소드가 필요하고, 결국 이 메소드를 사용하려면 user에 붙여서 사용해야함 (#14.3)
            if user.check_password(password):
                return self.cleaned_data  # 로그인 정보 모두 맞다면 cleaned_data 에 retuen 할 수 있도록
            else:
                # add.add_error(field,error) ? 에러가 뜬 곳이 어딘지 보고 싶을 때, password에서 에러가 뜬다면 모든 곳에 에러를 뜨게 하지 않고 password에 에러가 뜨도록
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User Does not exist"))


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Passwrod confirmation does not match")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        # create_user(username,email,password) 메소드의 필수 인자 세개..! 나는 username==email할거기때문에 아래와같이 작성
        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()