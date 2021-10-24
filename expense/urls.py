from django.urls import path
from .views import AddExpense, CreateCategory, CreateMonth, ReportGeneration, ShowExpenses

app_name = "expense"


urlpatterns = [
    path('add/', AddExpense.as_view(), name='add'),
    path('category/', CreateCategory.as_view(), name='category'),
    path('add_month/', CreateMonth.as_view(), name='add_month'),
    path('report/', ReportGeneration.as_view(), name='report'),
    path('search/', ShowExpenses.as_view(), name='search'),
]
