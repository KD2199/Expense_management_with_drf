
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer Class For User Model.
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    active = serializers.BooleanField(source='is_active', read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField(required=True, allow_null=False, allow_blank=False,
                                                      validators=[UniqueValidator(queryset=User.objects.all(), message='email already exists!')])
        self.fields['first_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['last_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'first_name', 'last_name', 'active']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer Class For User Register.
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    active = serializers.BooleanField(source='is_active', read_only=True)
    access_token = serializers.CharField(required=False, read_only=True)
    refresh_token = serializers.CharField(required=False, read_only=True)
    success = serializers.CharField(required=False, read_only=True)

    def __init__(self, *args, **kwargs):
        super(UserRegisterSerializer, self).__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True,
                                                        validators=[UniqueValidator(queryset=User.objects.all(), message='username already exists!')])
        self.fields['email'] = serializers.EmailField(required=True, allow_null=False, allow_blank=False,
                                                      write_only=True, validators=[UniqueValidator(queryset=User.objects.all(), message='email already exists!')])
        self.fields['password'] = serializers.CharField(required=False, write_only=True)
        self.fields['first_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True)
        self.fields['last_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'password', 'email', 'first_name', 'last_name',
                  'active', 'success', 'access_token', 'refresh_token']

    # JWT Token Generation
    def create(self, validated_data):
        """
        return user validate data
        """
        request = self._kwargs['context']['request']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        category_list = ['Fuel', 'Bill', 'Entertainment', 'Education', 'Food']
        for category in category_list:
            user.user_categories.get_or_create(name=category)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        token = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        user.is_logged_in = True
        user.save()
        validated_data["access_token"] = token['access']
        validated_data["refresh_token"] = token['refresh']
        validated_data["success"] = f'Hello {user} you have signup in successfully!!'
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer Class For Reset Password Of User Account.
    """
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access_token = serializers.CharField(required=False, read_only=True)
    refresh_token = serializers.CharField(required=False, read_only=True)
    success = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'success', 'access_token', 'refresh_token']

    def get_user_request(self):
        request = self._kwargs['context']['request']
        return request

    # JWT Token Generation
    def create(self, validated_data):
        """
        return token after user login successfully.
        """
        request = self.get_user_request()
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            user.is_logged_in = True
            user.save()
            validated_data["access_token"] = token['access']
            validated_data["refresh_token"] = token['refresh']
            validated_data["success"] = f'Hello {user} you have logged in successfully!!'
            return validated_data

        raise serializers.ValidationError({'error': 'You have entered invalid credentials!!'})


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer Class For Change Password Of User Account.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    success = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password', 'success']

    def update(self, instance, validated_data):
        user = instance
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')
        confirm_password = validated_data.get('confirm_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({'error': 'old password is incorrect!'})

        if new_password != confirm_password:
            raise serializers.ValidationError({'error': 'new password and confirm password not matched!'})

        user = User.objects.get(username=user)
        user.set_password(new_password)
        user.save()
        validated_data['success'] = 'Password Changed Successfully!'
        return validated_data


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Serializer Class For Reset Password Of User Account.
    """
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    success = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['new_password', 'confirm_password', 'success']

    def update(self, instance, validated_data):
        user = instance
        new_password = validated_data.get('new_password')
        confirm_password = validated_data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({'error': 'new password and confirm password not matched!'})

        user = User.objects.get(username=user)
        user.set_password(new_password)
        user.save()
        validated_data['success'] = 'Password Reset Successfully!'
        return validated_data
