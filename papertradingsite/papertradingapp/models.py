from django.db import models # type: ignore

nl = '\n'

# Create your models here.
class UserBalance(models.Model):
    first_name = models.TextField(max_length=70)
    last_name = models.TextField(max_length=70)
    balance = models.DecimalField(default=2000.00, decimal_places=2, max_digits=9)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Stock(models.Model):
    user_balance = models.ForeignKey(UserBalance, on_delete=models.CASCADE)
    stock_ticker = models.CharField(max_length=4)
    quantity = models.IntegerField(default=0)
    stock_value = models.DecimalField(decimal_places=2, max_digits=9)
    buy = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Ticker - {self.stock_ticker} - Value - {self.stock_value} - Owned - {self.quantity}"