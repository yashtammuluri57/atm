from django.db import models

# Create your models here.
class Customer(models.Model):
    username=models.CharField(max_length=40,unique=True)
    password=models.CharField(max_length=20)
    balance=models.FloatField(default=0)
    upi_pin=models.IntegerField(max_length=6)
class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    t_type = models.CharField(max_length=10)  # DEPOSIT / WITHDRAW
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
