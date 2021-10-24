"""api URL Configuration
"""

from django.urls import path
from account.api import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView,)

urlpatterns = [

    # JWT Authentication
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.UserRegisterView.as_view(), name='signup'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', views.ChangePasswordView.as_view(), name='password_change'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('profile/', views.UserProfileView.as_view(), name='user_detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
