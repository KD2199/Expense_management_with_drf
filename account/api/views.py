from rest_framework import status
from rest_framework.generics import (RetrieveUpdateAPIView,
                                     CreateAPIView, UpdateAPIView)
from rest_framework.permissions import (IsAuthenticated,)
from django.contrib.auth import get_user_model, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from account.api.permissions import IsLoggedIn

from account.api import serializers


User = get_user_model()


class UserRegisterView(CreateAPIView):
    """
    A view for user registration.
    """
    serializer_class = serializers.UserRegisterSerializer
    queryset = User.objects.all()


class UserLoginView(CreateAPIView):
    """
    A view for user login.
    """
    serializer_class = serializers.UserLoginSerializer
    queryset = User.objects.all()


class UserProfileView(RetrieveUpdateAPIView):
    """
    A view for viewing and editing user details.
    """
    permission_classes = [IsAuthenticated, IsLoggedIn]
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user = request.user
        user_data = request.data
        user_serializer = self.serializer_class(user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response({'success': 'Profile Update Successfully!'})


class ChangePasswordView(UpdateAPIView):

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated, IsLoggedIn]

    def get_object(self):
        user = self.request.user
        return user


class ResetPasswordView(UpdateAPIView):
    """
    A view for user registration.
    """
    serializer_class = serializers.ResetPasswordSerializer
    permission_classes = [IsAuthenticated, IsLoggedIn]

    def get_object(self):
        user = self.request.user
        return user


class LogoutView(APIView):
    permission_classes = (IsAuthenticated, IsLoggedIn)

    def get(self, request):
        success = {'success': f'{self.request.user} you have Logout Successfully!'}
        user = request.user
        logout(request)
        user.is_logged_in = False
        user.save()
        return Response(success, status=status.HTTP_205_RESET_CONTENT)

