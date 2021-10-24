from django.contrib.auth import get_user_model
from django.core import mail
import datetime
import random
import pytest


User = get_user_model()


class TestUrls:

    def add_test_data(self):
        """
        return user expenses.
        """
        income = random.randint(1000, 10000)
        limit = random.randint(1000, 10000)
        user = User.objects.create(username='test', password='test@123')
        user.expense_months.create(user=user, name='january', income=income, limit=limit, trigger='4000')
        user.user_categories.create(user=user, name='Fuel')
        category = user.user_categories.name
        result = 0
        for val in range(5):
            amount = random.randint(1000, 10000)
            result += amount
            user.user_expenses.create(user=user, type='expense', expense_category=category, amount=amount, date=datetime.datetime.now())
        data = user.user_expenses.filter(user=user)
        budget = user.expense_months.get(name='january')
        budget.limit -= result
        budget.save()
        return data, user

    @pytest.mark.django_db
    def test_user_login(self, client):
        """
        return user status after login.
        """
        user = User.objects.create(username='test', password='test@123')
        client.force_login(user)
        assert user.is_authenticated

    @pytest.mark.django_db
    def test_get_expenses(self):
        """
        return assert True if limit is exceed .
        """
        user_expense, user = self.add_test_data()
        total_amount = 0
        for item in user_expense:
            total_amount += float(item.amount)
        limit = float(user.expense_months.get(name='january').limit)
        assert 'True' if total_amount > limit else 'False'

    def test_an_admin_view(self, admin_client):
        """
        return status after admin login.
        """
        response = admin_client.get('/admin/')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_search_expenses(self, client):
        """
        search expenses if user is authenticate.
        """
        response = client.get('/expense/search/', {'q': 'expense'})
        assert response.status_code == 302

    def test_mail(self, mailoutbox):
        mail.send_mail('subject', 'body', 'from@example.com', ['to@example.com'])
        assert len(mailoutbox) == 1
        m = mailoutbox[0]
        print(f'\n------ mail list {m.to} ------')
        assert m.subject == 'subject'
        assert m.body == 'body'
        assert m.from_email == 'from@example.com'
        assert list(m.to) == ['to@example.com']