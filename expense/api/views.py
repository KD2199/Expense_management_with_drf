
from rest_framework.generics import (ListAPIView, ListCreateAPIView,)
from rest_framework.permissions import (IsAuthenticated,)
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from expense.api import serializers
from django.db.models import Q, Sum
from account.api.permissions import IsLoggedIn

User = get_user_model()


class CategoryView(ListCreateAPIView):
    """
    A view for create and list user categories.
    """
    serializer_class = serializers.CategoriesSerializer
    permission_classes = [IsAuthenticated, IsLoggedIn]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        return user.user_categories.all()


class MonthView(ListCreateAPIView):
    """
    A view for create and list user expense months.
    """
    serializer_class = serializers.MonthSerializer
    permission_classes = [IsAuthenticated, IsLoggedIn]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        return user.expense_months.all()


class ExpensesView(ListCreateAPIView):
    """
    A view for create and list user expenses.
    """
    serializer_class = serializers.ExpenseSerializer
    permission_classes = [IsAuthenticated, IsLoggedIn]

    def get_queryset(self):
        user = self.request.user
        return user.user_expenses.all()

    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.get_queryset()
        serializer = serializers.ExpenseSerializer(queryset, many=True)
        expenses = user.user_expenses
        total_income = expenses.filter(type='income').aggregate(Sum('amount'))
        total_expense = expenses.filter(type='expense').aggregate(Sum('amount'))
        data = serializer.data

        if data:
            total_inc = 0
            total_exp = 0
            res = {}
            if total_income['amount__sum']:
                total_inc = total_income['amount__sum']
            if total_expense['amount__sum']:
                total_exp = total_expense['amount__sum']
            total = {
                'total_income': total_inc,
                'total_expense': total_exp
            }
            # data.append(total)
            res['expense_data'] = data
            res['total'] = total
            return Response(data=res)
        return Response({'message': 'Expense Data Not found!'}, status=404)


class SearchView(ListAPIView):
    """
    A view for Listing expenses based on user search .
    """
    serializer_class = serializers.ExpenseSerializer
    permission_classes = [IsAuthenticated, IsLoggedIn]

    def get_queryset(self):
        query = self.request.GET.get('q')
        user = self.request.user
        object_list = user.user_expenses.filter(
            (Q(type__icontains=query) | Q(expense_category__name__icontains=query))).order_by('date')

        return object_list

