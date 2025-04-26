from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shop_users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='shop_users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='shop_users/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='shop_users/password_change_done.html'), name='password_change_done'),
]