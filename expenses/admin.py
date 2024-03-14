from django.contrib import admin

# Register your models here.
from expenses.models import *


from django.contrib import admin
from .models import User, Expense, ExactExpense, PercentExpense

# Register your models here.
admin.site.register(User)
admin.site.register(Expense)
admin.site.register(ExactExpense)
admin.site.register(PercentExpense)