from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('expanses/', views.index, name="expenses"),
    path('add-expense', views.add_expense, name='add-expenses'),
    path('edit-expense/<int:id>', views.expense_edit, name='expense-edit'),
    path('delete-expense/<int:id>', views.delete_expense, name='expense-delete'),




]

