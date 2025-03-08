from django import forms
from .models import StandardUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class StandardUserCreationForm(UserCreationForm):
    class Meta: 
        model = StandardUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'name',
            'surname',
        ]

class StandardLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.PasswordInput(attrs={'class':'form-control'})