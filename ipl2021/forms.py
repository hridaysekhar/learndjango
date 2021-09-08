from django import forms
from .models import *


class NameForm(forms.Form):
    name = forms.CharField(label="Username", max_length=100)

    def save(self):
        pass


class UserForm(forms.Form):
    class Meta:
        model = UserDetails
        print('In Here')
        fields = ['username','password']