
from django import forms
from django.contrib.auth import get_user_model
from .models import Expenses, Categories, ExpenseMonths
from templatetags.get_month_name import get_month
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.http import HttpResponse
import csv

User = get_user_model()


class UserExpenseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super(UserExpenseForm, self).__init__(*args, **kwargs)
        self.fields['expense_category'].queryset = (self.user.user_categories.all())

    class Meta:
        model = Expenses
        fields = ('type', 'expense_category', 'amount', 'date')

        widgets = {'type': forms.Select(attrs={'onchange': "check()"}),
                   'expense_category': forms.Select(attrs={'class': 'regDropDown', 'placeholder': _(' Select Category')}),
                   'amount': forms.NumberInput(attrs={'class': 'form-group', 'placeholder': _(' Enter Amount')}),
                   'date': forms.DateInput(attrs={'class': 'form-group', 'type': 'date'}),
                   }

    def clean_amount(self):
        price = self.cleaned_data['amount']
        if price < 0:
            raise forms.ValidationError("Amount can't be negative")
        return price

    def save(self, commit=True):
        instance = super(UserExpenseForm, self).save(commit=False)
        instance.user = self.user
        name = str(self.cleaned_data.get("date"))
        name = get_month(name.split('-')[1])
        data = self.user.expense_months.filter(name=name)
        for value in data:
            if instance.type == 'income':
                value.income += Decimal(instance.amount)
            else:
                value.limit -= Decimal(instance.amount)
            value.save()
        instance.save()
        return instance


class NewCategoryForm(forms.Form):

    new_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': _(' Enter Category Name')}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super(NewCategoryForm, self).__init__(*args, **kwargs)

    def save(self):
        category_name = self.cleaned_data.get('new_category')
        categories = self.user.user_categories.filter(name=category_name).exists()
        if not categories:
            Categories.objects.create(user=self.user, name=category_name)
            return True
        return False


class AddMonthForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super(AddMonthForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ExpenseMonths
        fields = ('name', 'income', 'limit')

        widgets = {
                   'name': forms.NumberInput(attrs={'class': 'form-group', 'type': 'month'}),
                   'limit': forms.NumberInput(attrs={'class': 'form-group', 'placeholder': _(' Set Your This Month Limit')}),
                   'income': forms.NumberInput(attrs={'class': 'form-group', 'placeholder': _(' Enter Your This Month Income')}),
                   }

    def clean_income(self):
        income = self.cleaned_data['income']
        if income < 0:
            raise forms.ValidationError("Income can't be negative")
        return income

    def clean_limit(self):
        price = self.cleaned_data['limit']
        if price < 0:
            raise forms.ValidationError("Limit can't be negative")

        return price

    def clean(self):
        name = self.cleaned_data.get("name")
        if name:
            name = get_month(name.split('-')[1])
            self.cleaned_data["name"] = name
        return self.cleaned_data

    def save(self, commit=True):
        instance = super(AddMonthForm, self).save(commit=False)
        instance.user = self.user
        trigger = (instance.limit*10)/100
        instance.trigger = trigger
        instance.save()
        return instance


class GenerateReport(forms.Form):

    start_date = forms.DateTimeField(widget=forms.NumberInput(attrs={'type': 'date'}))
    end_date = forms.DateTimeField(widget=forms.NumberInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super(GenerateReport, self).__init__(*args, **kwargs)

    def save(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        user = self.user
        data = user.user_expenses.filter(date__gt=start_date, date__lte=end_date).order_by('date')
        if data:
            response = HttpResponse(content_type='text/csv')
            file_name = f"{user.get_full_name()}_{start_date.strftime('%d-%m-%Y')}_{end_date.strftime('%d-%m-%Y')}_expenses.csv"
            response['Content-Disposition'] = f'attachment; filename={file_name}'

            header = ['User', 'Type', 'Category', 'Amount', 'Date']
            total_income = 0
            total_expense = 0
            writer = csv.writer(response)
            writer.writerow(header)
            for field in data:
                if field.expense_category:
                    total_expense += float(field.amount)
                    row = [user.get_full_name(), field.type, field.expense_category.name, float(field.amount),
                           field.date.strftime('%d-%m-%Y')]
                    writer.writerow(row)
                else:
                    total_income += float(field.amount)
                    row = [user.get_full_name(), field.type, '-', float(field.amount), field.date.strftime('%d-%m-%Y')]
                    writer.writerow(row)

            writer.writerow([])
            income = ['', '', '', f'Total Income: {total_income}', '']
            expenses = ['', '', '', f'Total Expense: {total_expense}', '']
            writer.writerow(income)
            writer.writerow(expenses)

            return response

        return None

