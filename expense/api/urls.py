"""api URL Configuration
"""

from django.urls import path
from expense.api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='add_category'),
    path('month/', views.MonthView.as_view(), name='add_month'),
    path('expenses/', views.ExpensesView.as_view(), name='expenses'),
    path('search/', views.SearchView.as_view(), name='search'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
