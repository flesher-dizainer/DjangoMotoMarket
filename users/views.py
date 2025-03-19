from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser


# Создадим представление регистрации пользователя
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(request, 'нужно написать страницу')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # После успешной регистрации перенаправляем пользователя на страницу входа
        return response

class CustomLogoutView(LogoutView):
    """Представление для выхода пользователей"""
    #next_page = reverse_lazy('core:index')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().post(request, *args, **kwargs)
