# tasks.py
import os
import csv
from datetime import datetime
from celery import shared_task
from django.conf import settings
from .models import User, Expense

@shared_task
def backup_user_data():
    # Retrieve all users and their expenses
    users = User.objects.all()
    expenses = Expense.objects.all()

    # Generate CSV data
    csv_data = [['User ID', 'Name', 'Email', 'Mobile Number', 'Expense ID', 'Amount', 'Type']]

    for user in users:
        for expense in expenses.filter(user=user):
            csv_data.append([user.userId, user.name, user.email, user.mobile_number, expense.amount, expense.expense_type])

    # Create backup directory if it doesn't exist
    backup_dir = 'backup'
    os.makedirs(backup_dir, exist_ok=True)

    # Create CSV file with timestamp in filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'user_data_{timestamp}.csv'
    filepath = os.path.join(backup_dir, filename)

    # Write CSV data to file
    with open(filepath, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(csv_data)

    return filepath
