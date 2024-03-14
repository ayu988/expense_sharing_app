from django.db import models
import uuid

def generate_user_id():
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    # Convert UUID to base64 encoded string
    encoded_uuid = random_uuid.bytes.hex()[:5]  # Take first 5 characters for a 5-digit code
    # Remove non-alphanumeric characters and convert to uppercase
    alphanumeric_code = ''.join(c for c in encoded_uuid if c.isalnum()).upper()
    return alphanumeric_code

# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=5, primary_key=True, default=generate_user_id)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.userId
    

class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'

    EXPENSE_TYPES = [
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=10, choices=EXPENSE_TYPES)

    # Add more fields as needed

    def __str__(self):
        return f"{self.user.name}'s Expense"
    
class ExactExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=10, decimal_places=2)

class PercentExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)