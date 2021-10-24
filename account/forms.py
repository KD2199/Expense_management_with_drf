
from expense.models import Categories
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django import forms

User = get_user_model()


class UserSignUp(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'email', 'password')
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': _('Enter Username')}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': _('Enter First Name')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': _('Enter Last Name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': _('Enter Email')}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder': _('Enter Password')}),
        }

        error_messages = {
            'username': {
                'unique': _('Username is already exists!'),
            },
            'email': {
                'unique': _('Email is already exists!'),
            },
            'password': {
                'unique': _('Your password should be at least 6 Characters!'),
            },
        }

    def clean_password(self):
        password = self.cleaned_data['password']
        if validate_password(password, self.instance):
            raise forms.ValidationError("Your password should be at least 6 Characters")
        return password

    def save(self, commit=True):
        category_list = ['Fuel', 'Bill', 'Entertainment', 'Education', 'Food']
        user = super(UserSignUp, self).save(commit=commit)
        user.set_password(self.cleaned_data["password"])
        user.save()
        for category in category_list:
            Categories.objects.create(user=user, name=category)
        return user


class UserProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'email', 'profile_image')
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': _('Enter Username')}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': _('Enter First Name')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': _('Enter Last Name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder': _('Enter Email')}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

        error_messages = {
            'username': {
                'unique': _('Username is already exists!'),
            },
            'email': {
                'unique': _('Email is already exists!'),
            },
        }

    def save(self, commit=True):
        user = super(UserProfile, self).save(commit=commit)
        return user
