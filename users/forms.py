from django import forms
from . import models

# 내가 이 폼 안에서 할 것 은 모든 로그인과 회원가입을 Django 안에서 username == email 이도록 설정할 것임
class LoginForm(forms.Form):
    email = forms.EmailField()
    # forms. 해보면 PasswordInput 이라는 메소드도 뜨는데, 이 Input 은 Field와는 다르대. 암튼 나는 캐릭터필드안에서 조건을 생성해주도록 하겠음
    password = forms.CharField(widget=forms.PasswordInput)

    # clean() 을 사용한다면 한 필드에 직접 에러를 추가해 주어야 한다.
    # clean_password(), clean_username() 처럼 이전 커밋과 같이 쓸거면 그냥 error를 raise 하면 되지만,
    # clean()으로 합쳐(?) 사용할 땐 raise 가 아닌 어느 특정 필드에서 에러가 난지 알아야 하기 때문에, 필드마다 직접 에러추가 해주어야함
    # 또한, clean() 을 사용할 땐 "언제나 무조건!! " cleaned_data 를 return 해야함
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(
                email=email  # 나중에 모든 계정에 대한 username과 email이 같에 할거지만, 지금은 에러때문에 잠시 email=email로 변경
            )  # check_password 메소드 ? 패스워드를 확인하기 위해서는 user의 정보가 필요할 것이다. 때문에 이 메소드가 필요하고, 결국 이 메소드를 사용하려면 user에 붙여서 사용해야함 (#14.3)
            if user.check_password(password):
                return self.cleaned_data  # 로그인 정보 모두 맞다면 cleaned_data 에 retuen 할 수 있도록
            else:
                # add.add_error(field,error) ? 에러가 뜬 곳이 어딘지 보고 싶을 때, password에서 에러가 뜬다면 모든 곳에 에러를 뜨게 하지 않고 password에 에러가 뜨도록
                self.add_error("password", forms.ValidationError("Password is wrong"))
        # email과 password는 서로에게 종속 되어 있으므로 아래 except 부분에 userError을 띄우도록 수정
        except models.User.DoesNotExist:
            self.add_error(forms.ValidationError("User Does not exist"))
