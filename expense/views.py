from django.contrib.auth import get_user_model
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView, UpdateView
from .forms import UserExpenseForm, NewCategoryForm, AddMonthForm, GenerateReport
from django.utils.translation import gettext_lazy as _
from django.shortcuts import HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from templatetags.get_month_name import get_month
from .models import Expenses, ExpenseMonths
from django.contrib import messages
from django.db.models import Q

User = get_user_model()


class CreateCategory(LoginRequiredMixin, FormView):

    template_name = 'expense/addcategory.html'
    form_class = NewCategoryForm
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        flag = form.save()
        if flag:
            messages.success(self.request, f'New Category Created !')
            return HttpResponseRedirect('/')

        messages.info(self.request, f'Category Already Created !')
        return redirect('expense:category')


class AddExpense(LoginRequiredMixin, CreateView):

    template_name = 'expense/expense.html'
    form_class = UserExpenseForm
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        name = str(form.cleaned_data.get("date"))
        name = get_month(name.split('-')[1])

        if user.expense_months.filter(name=name).exists():
            form.save()
            expense_type = form.cleaned_data.get("type")
            messages.success(self.request, f'{expense_type} Added successfully!')
            return HttpResponseRedirect('/')
        messages.info(self.request, f'Expenses Month Not Found !')
        return HttpResponseRedirect('/')


class CreateMonth(LoginRequiredMixin, CreateView):

    template_name = 'expense/month.html'
    form_class = AddMonthForm
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):

        month_name = form.cleaned_data['name']
        user = self.request.user
        check = user.expense_months.filter(name=month_name).exists()

        if not check:
            form.save()
            messages.success(self.request, 'Month Added successfully!')
            return HttpResponseRedirect('/')
        messages.info(self.request, 'Expense Month Already Exists!')
        return redirect('expense:add_month')


class ShowExpenses(LoginRequiredMixin, ListView):

    template_name = 'expense/show.html'
    model = Expenses
    context_object_name = 'result'
    login_url = '/login/'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        user = self.request.user
        object_list = user.user_expenses.filter((Q(type__icontains=query) | Q(expense_category__name__icontains=query)) &
                                               (Q(user__username__icontains=self.request.user))).order_by('date')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class ReportGeneration(LoginRequiredMixin, FormView):

    template_name = 'expense/report.html'
    form_class = GenerateReport
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        flag = form.save()
        if flag:
            return flag
        messages.info(self.request, f'No Data Found!')
        return redirect('expense:report')


