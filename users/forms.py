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


# ModelForm 자체에 clean, save 메소드가 존재함 !!!! 때문에 email field, clean_email 이 필요 없다. 알아서 해준다 . + unique 한 field 값을 validate 할 수도 있음
class SignUpForm(forms.ModelForm):
    # ModelForm 틀에 관한 것 (#15.2)
    class Meta:
        model = models.User
        # 아래 fields 안에 선언하는 필드가 알아서 html 에 form 형태로 뜸
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Passwrod confirmation does not match")
        else:
            return password

    # ModelForm 에서 이미 갖고 있는 save 메소드에다가 override 하기 (username을 email로)
    def save(self, *args, **kwargs):
        # commit=False?  Django object 는 생성되지만 그 object이 데이터베이스에 올라가지는 않게 하기 위한 옵션. 즉 , user은 만들지만 save는 하지마!
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email  # user 의 username 값이 email이 되도록 해주었다
        user.set_password(password)  # 사용자 비밀번호를 암호화해서 저장하는 메소드
        user.save()
