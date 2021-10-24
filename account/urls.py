from django.urls import path
from .views import Home, Signup, Profile, UserLoginView
from django.contrib.auth import views as auth_views

app_name = "account"


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("<slug>/profile", Profile.as_view(), name="profile"),
    path("signup/", Signup.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name="PasswordChange"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset/done/', UserLoginView.as_view(), name="password_reset_complete"),
]
