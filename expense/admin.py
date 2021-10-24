from django.contrib import admin
from .models import Expenses, Categories, ExpenseMonths


@admin.register(Expenses)
class Expenses(admin.ModelAdmin):
    list_display = ('user', 'type', 'expense_category')
    list_filter = ['user']


@admin.register(Categories)
class Categories(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ['user']


@admin.register(ExpenseMonths)
class ExpenseMonths(admin.ModelAdmin):
    list_display = ('user', 'name')
    list_filter = ['user']
