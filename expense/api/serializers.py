from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from expense.models import Categories, ExpenseMonths, Expenses


User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    """
    Serializer Class For Categories Model.
    """
    class Meta:
        model = Categories
        fields = ['id', 'name']

    def get_user(self):
        request = self._kwargs['context']['request']
        user = request.user
        return user

    def validate_name(self, value):
        user = self.get_user()
        if value is not None:
            category_exist = user.user_categories.filter(name=value).exists()
            if category_exist:
                raise serializers.ValidationError("Category Already Exists!")
        return value


class MonthSerializer(serializers.ModelSerializer):
    """
    Serializer Class For ExpenseMonths Model.
    """
    trigger = serializers.FloatField(required=False, write_only=True)

    class Meta:
        model = ExpenseMonths
        exclude = ('user',)

    def get_user(self):
        request = self._kwargs['context']['request']
        user = request.user
        return user

    def validate_name(self, value):
        user = self.get_user()
        if value is not None:
            month_exist = user.expense_months.filter(name=value).exists()
            if month_exist:
                raise serializers.ValidationError("Expense Month Already Exists!")
        return value

    def validate(self, attrs):
        data = attrs
        limit = data['limit']
        data['trigger'] = (limit*10)/100
        return data


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer Class For Expenses Model.
    """
    expense_category = serializers.CharField(required=False)
    date = serializers.DateField(required=False, default=None)

    class Meta:
        model = Expenses
        fields = ['id', 'type', 'amount', 'date', 'expense_category']

    def get_user(self):
        request = self._kwargs['context']['request']
        user = request.user
        return user

    def validate_expense_category(self, value):
        user = self.get_user()
        if value is not None:
            category_exist = user.user_categories.filter(name=value).exists()
            if not category_exist:
                raise serializers.ValidationError("Expense Category Not Exists!")
            value = list(user.user_categories.filter(name=value))[0]
        return value

    def validate_date(self, value):
        user = self.get_user()
        if value is not None:
            name = value.strftime("%B")
        else:
            value = timezone.now().date()
            name = value.strftime("%B")
        month_exist = user.expense_months.filter(name=name).exists()
        if not month_exist:
            raise serializers.ValidationError("Expense Month Not Exists!")
        return value

    def validate_amount(self, value):
        if value is not None:
            if float(value) < 0:
                raise serializers.ValidationError("Amount Can't be negative!")
        return value

    def create(self, validated_data):
        user = self.get_user()
        user.user_expenses.create(user=user, **validated_data)
        name = validated_data.get('date').strftime("%B")
        amount = validated_data.get('amount')
        expense_type = validated_data.get('type')
        data = user.expense_months.get(name=name)
        if expense_type == 'expense':
            data.limit -= Decimal(amount)
        else:
            data.income += Decimal(amount)
        data.save()
        return validated_data

