from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('login/telegram/', views.LoginWithTelegramView.as_view(), name='login_telegram'),
    path('check_auth/', views.CheckAuthView.as_view(), name='check_auth'),
    path('authenticate/', views.AuthenticateTelegramView.as_view(), name='authenticate'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
