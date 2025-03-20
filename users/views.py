from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import CustomUser


# Создадим представление регистрации пользователя
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(request, 'Вы уже зарегистрированы и вошли в систему.')
            return redirect('core:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти в систему.')
        return response


class CustomLoginView(LoginView):
    """Представление для входа пользователей"""
    template_name = 'users/login.html'
    next_page = reverse_lazy('core:index')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'Вы уже вошли в систему!')
            return redirect('core:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Представление для выхода пользователей"""
    next_page = reverse_lazy('core:index')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().post(request, *args, **kwargs)


class ProfileView(DetailView):
    """Представление для просмотра профиля пользователя"""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return get_object_or_404(CustomUser, username=self.kwargs.get('username'))


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя"""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile_edit.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    """Представление для сброса пароля"""
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Представление для страницы успешной отправки письма для сброса пароля"""
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Представление для установки нового пароля"""
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    form_class = CustomSetPasswordForm


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Представление для страницы успешного сброса пароля"""
    template_name = 'users/password_reset_complete.html'
