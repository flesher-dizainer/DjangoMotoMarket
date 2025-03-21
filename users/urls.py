from django.urls import path
from .views import (
    RegisterView, CustomLogoutView, CustomLoginView,
    ProfileView, ProfileEditView,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
    UserListView, ChangeUserTypeView
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Профиль пользователя
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<str:username>/edit/', ProfileEditView.as_view(), name='admin_profile_edit'),

    # Администрирование пользователей
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<str:username>/change-type/', ChangeUserTypeView.as_view(), name='change_user_type'),

    # Восстановление пароля
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
