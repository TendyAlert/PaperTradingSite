from django.db import models # type: ignore
from django.contrib.auth.models import User #type: ignore

# Create your models here.
    
class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user_balance = models.DecimalField(decimal_places=2, default=2000.00, max_digits=9)
    stock_ticker = models.CharField(max_length=4)
    quantity = models.IntegerField(default=0)
    stock_value = models.DecimalField(decimal_places=2, max_digits=9)
    buy = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Ticker - {self.stock_ticker} - Value - {self.stock_value} - Owned - {self.quantity}"