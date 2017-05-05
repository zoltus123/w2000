from django import forms
from .models import WynikKandydata

class GminyForm(forms.Form):
    wzorzec = forms.CharField(label='Podaj nazwę gminy:', max_length=100)

class loginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika:')
    password = forms.CharField(label='Hasło:', widget=forms.PasswordInput)

class wynikForm(forms.Form):
    wynik = forms.IntegerField(label='Wynik:', min_value=0)