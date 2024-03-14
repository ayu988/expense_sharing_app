from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Expense
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
import json
from decimal import Decimal
from .models import User, Expense, ExactExpense, PercentExpense
from django.db import transaction

# Create your views here.
def list_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_list = [{'userId': user.userId, 'name': user.name, 'email': user.email, 'mobile_number': user.mobile_number} for user in users]
        return JsonResponse({'users': user_list})
    return JsonResponse({'error': 'GET request required.'}, status=400)


def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            mobile_number = data.get('mobile_number')

            # Check if a user with the given email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'User with this email already exists.'}, status=400)

            # Create the user
            user = User.objects.create(name=name, email=email, mobile_number=mobile_number)
            return JsonResponse({'message': 'User added successfully.', 'user_id': user.userId})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'POST request required.'}, status=400)

@transaction.atomic
def add_expense(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            amount = data.get('amount')
            expense_type = data.get('expense_type')
            shares = data.get('shares')

            user = get_object_or_404(User, userId=user_id)

            if expense_type == 'EXACT':
                total_shares = sum(shares.values())
                if total_shares != amount:
                    return JsonResponse({'error': 'Total shares must equal the amount for EXACT expense type.'}, status=400)
                expense = Expense.objects.create(user=user, amount=amount, expense_type=expense_type)
                for friend_id, share_amount in shares.items():
                    friend = get_object_or_404(User, userId=friend_id)
                    ExactExpense.objects.create(user=friend, expense=expense, share=share_amount)
            elif expense_type == 'PERCENT':
                total_percent = sum(shares.values())
                if total_percent != 100:
                    return JsonResponse({'error': 'Total percentage shares must equal 100 for PERCENT expense type.'}, status=400)
                expense = Expense.objects.create(user=user, amount=amount, expense_type=expense_type)
                for friend_id, percent_share in shares.items():
                    friend = get_object_or_404(User, userId=friend_id)
                    amount_share = (amount * percent_share) / 100
                    PercentExpense.objects.create(user=friend, expense=expense, percentage=percent_share)

            new_expense = Expense.objects.create(user=user, amount=amount, expense_type=expense_type)
            return JsonResponse({'message': 'Expense added successfully.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

    return JsonResponse({'error': 'POST request required.'}, status=400)

def user_expenses(request, user_id):
    user = get_object_or_404(User, userId=user_id)
    expenses = Expense.objects.filter(user=user)
    data = [{'amount': expense.amount, 'expense_type': expense.expense_type} for expense in expenses]
    return JsonResponse({'expenses': data})

def show_balances(request):
    users = User.objects.all()
    balances = {}

    # Calculate total expenses for each user
    total_expenses = {user.userId: user.expense_set.aggregate(total=Sum('amount'))['total'] or Decimal('0.00') for user in users}

    # Calculate balances between users
    for user in users:
        user_balance = {}
        total_spent = total_expenses[user.userId]

        for friend in users.exclude(userId=user.userId):
            friend_total_expense = total_expenses[friend.userId]
            balance = friend_total_expense - total_spent

            if balance != Decimal('0.00'):
                user_balance[friend.name] = balance

        balances[user.name] = user_balance

    return JsonResponse({'balances': balances})