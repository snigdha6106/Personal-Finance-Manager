# models.py
from django.db import models
from django.contrib.auth.models import User
from home.models import User  # Replace `myapp` with your actual app name
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('budget', 'Budget'),
    ]
    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    is_custom = models.BooleanField(default=False)  # To track if the category is custom or predefined
    def __str__(self):
        return self.name
class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('Income', 'Income'), ('Expense', 'Expense')])
    def __str__(self):
        return f'{self.description} - {self.amount}'

