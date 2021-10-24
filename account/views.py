
import random
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .forms import UserProfile, UserSignUp
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Home(LoginRequiredMixin, TemplateView):

    login_url = '/login/'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['month_list'] = list(user.expense_months.order_by('name'))
        category_list = list(user.user_categories.values_list('name', flat=True))
        labels = []
        data = []
        color = []

        for cat in category_list:
            amounts = list(user.user_expenses.filter(type='expense', expense_category__name=cat)
                           .values_list('amount', flat=True))
            total = float(sum(amounts))
            if total > 0:
                labels.append(cat)
                data.append(total)
                red, green, blue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                color.append(f'rgba({red},{green},{blue})')
        context['labels'], context['data'], context['color'] = labels, data, color
        return context


class Signup(FormView):

    template_name = 'account/signup.html'
    form_class = UserSignUp

    def form_valid(self, form):
        form.save()
        msg = _('Hello! You were successfully SignUp!')
        messages.success(self.request, msg)
        return HttpResponseRedirect('/')


class Profile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = 'account/profile.html'
    success_url = 'profile'
    login_url = '/login/'
    model = User
    form_class = UserProfile
    success_message = _('Profile Update successfully !')


class UserLoginView(SuccessMessageMixin, LoginView):
    """
        User Login view
    """
    template_name = 'registration/login.html'
    success_message = _("Hello %(username)s! You were successfully logged in!")


