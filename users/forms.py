from django import forms

# 내가 이 폼 안에서 할 것 은 모든 로그인과 회원가입을 Django 안에서 username == email 이도록 설정할 것임
class LoginForm(forms.Form):
    email = forms.EmailField()
    # forms. 해보면 PasswordInput 이라는 메소드도 뜨는데, 이 Input 은 Field와는 다르대. 암튼 나는 캐릭터필드안에서 조건을 생성해주도록 하겠음
    password = forms.CharField(widget=forms.PasswordInput)