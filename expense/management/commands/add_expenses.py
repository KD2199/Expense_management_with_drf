import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from expense.models import Expenses
import csv

User = get_user_model()


class Command(BaseCommand):
    help = 'Displays all users'

    def handle(self, *args, **kwargs):
        with open('data.csv') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for row in data:
                user = User.objects.get(username=row[0])
                category = user.user_categories.get(name=row[2])
                date = datetime.datetime.strptime(row[4], '%d-%m-%Y').date()
                user.user_expenses.create(user=row[0], type=row[1], expense_category=category, amount=row[3], date=date)
        users = Expenses.objects.all()
        for user in users:
            self.stdout.write(f"{user.id}: {user}")
