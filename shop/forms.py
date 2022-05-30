from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Потверждение пароля"

    username = forms.CharField(max_length=30, required=True, label='Имя пользователя')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email = forms.CharField(max_length=30, required=True, label='Эл. Почта', error_messages={'invalid': 'Введите действительный эл. адрес'})
    phone_number = forms.CharField(max_length=30, required=True, label='Номер телефона')
    city = forms.CharField(max_length=30, required=True, label='Город')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'password1', 'password2')


class LoginAuthForm(forms.Form):
    username = forms.CharField(max_length=30, required=True, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True, label='Пароль')

