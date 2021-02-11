from django import forms
from . import models
from django_countries.fields import CountryField


class SearchForm(forms.Form):

    city = forms.CharField(initial="Any")
    country = CountryField(default="KR").formfield()
    price = forms.IntegerField(required=False)
    # <select>대신 사용하는 ModelChoiceField 는 쿼리셋을 필요로 하기 때문에 다음과 같이 쓴다.
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)

    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    # <input type=checkbox> 대신 사용하는 ModelMultipleChoiceField 도 쿼리셋을 필요로 하므로 다음과 같이 작성한다.
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
