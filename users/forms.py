from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# Регистрация пользователя
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone', 'email', 'user_type')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


# Редактирование профиля пользователя
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'avatar')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


# Форма изменения типа пользователя, только для админов
class ChangeUserTypeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('user_type',)
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }


# Форма фильтрации пользователей
class CustomerFilterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', required=False)
    email = forms.EmailField(label='Email', required=False)
    phone = forms.CharField(label='Телефон', required=False)
    user_type = forms.ChoiceField(label='Тип пользователя', choices=CustomUser.USER_TYPE_CHOICES, required=False)
