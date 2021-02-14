from django import forms
from . import models

# 내가 이 폼 안에서 할 것 은 모든 로그인과 회원가입을 Django 안에서 username == email 이도록 설정할 것임
class LoginForm(forms.Form):
    email = forms.EmailField()
    # forms. 해보면 PasswordInput 이라는 메소드도 뜨는데, 이 Input 은 Field와는 다르대. 암튼 나는 캐릭터필드안에서 조건을 생성해주도록 하겠음
    password = forms.CharField(widget=forms.PasswordInput)

    # clean_email은 내가 만든 이름이 아님.
    # 만약 이메일이나 빌번이 있는 필드를 확인하고 싶으면 method의 이름은 clean_ 이어야한다. (#14.2 참고하자 )
    # clean_ 으로 시작되는 method 들이 하는 일은 에러를 넣는 것 뿐만아니라 데이터를 정리도 해줌
    # 내가 만약 clean method 를 하나 만들었다면 , 근데 내가 아무것도 return 하지 않으면 그 field를 지워버린다. 따라서 return 해주어야해!
    # return 을 하면 field가 아직 유효하기에, cleaned_data 라는 메소드 안에서 field 를 볼 수 있다.
    # clean_data 는 정리의 결과물이라고 말할 수 있음
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # 유저를 가지고 왔는데 작동되지 않는다면, 유저가 없다는 뜻
        try:
            # username 은 email과 같에 할 것이기 때문에 아래와 같이 작성
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User dose not exist!")

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            # check_password 메소드 ? 패스워드를 확인하기 위해서는 user의 정보가 필요할 것이다. 때문에 이 메소드가 필요하고, 결국 이 메소드를 사용하려면 user에 붙여서 사용해야함
            if user.check_password(password):
                return password
            else:
                raise forms.ValidationError("Password is wrong")
        except models.User.DoesNotExist:
            pass