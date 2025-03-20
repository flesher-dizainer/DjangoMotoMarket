from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser


# Регистрация пользователя
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'avatar', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7XXXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтверждение пароля'})

        # Русификация подсказок
        self.fields['username'].help_text = 'Обязательное поле. До 150 символов. Только буквы, цифры и @/./+/-/_.'
        self.fields[
            'password1'].help_text = 'Пароль должен содержать не менее 8 символов и не должен быть слишком простым.'
        self.fields['password2'].help_text = 'Введите пароль повторно для подтверждения.'


# Редактирование профиля пользователя
class CustomUserChangeForm(UserChangeForm):
    password = None  # Убираем поле пароля из формы редактирования

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'avatar', 'bio', 'date_of_birth')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
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
    username = forms.CharField(label='Имя пользователя', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(
        label='Тип пользователя',
        choices=[('', 'Все')] + list(CustomUser.USER_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


# Кастомная форма сброса пароля
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'})
    )


# Кастомная форма установки нового пароля
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}),
    )
