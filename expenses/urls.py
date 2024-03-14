from django.urls import path
from . import views

urlpatterns = [
    path('add_expense/', views.add_expense, name='add_expense'),
    path('user_expenses/<str:user_id>/', views.user_expenses, name='user_expenses'),
    path('show_balances/', views.show_balances, name='show_balances'),
]
