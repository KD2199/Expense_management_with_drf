from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_categories')
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Expenses(models.Model):

    EXPENSE = "expense"
    INCOME = "income"

    CHOICES = (
        (EXPENSE, "Expense"),
        (INCOME, "Income"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_expenses')
    type = models.CharField(choices=CHOICES, default=EXPENSE, max_length=20)
    expense_category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='category_expenses', null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=5,)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} add {self.type} on {self.date.strftime('%d-%m-%Y')}"


class ExpenseMonths(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expense_months')
    name = models.CharField(max_length=10)
    limit = models.DecimalField(max_digits=15, decimal_places=2,)
    income = models.DecimalField(max_digits=15, decimal_places=2,)
    trigger = models.IntegerField()

    def __str__(self):
        return f"{self.user.get_full_name()}'s {self.name} Expenses"



