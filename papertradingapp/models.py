from django.db import models # type: ignore
from django.contrib.auth.models import User #type: ignore
from datetime import datetime, timedelta
from django.utils import timezone
import yfinance as yf #type: ignore

date = datetime.now()
delta = timedelta(weeks=13)
dateFourMonthsAgo = date - delta
# Create your models here.
    
class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, default=10000.00, max_digits=9)

    def __str__(self):
        return f"Balance for {self.user.username}"

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_ticker = models.CharField(default='null', max_length=5)
    bought_at = models.DecimalField(decimal_places=2, default=0.00, max_digits=9)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Ticker - {self.stock_ticker} - Bought at - {self.bought_at} - Owned - {self.quantity}"
    
class YFinanceData(models.Model):
    aapl = models.JSONField(default=dict)
    amd = models.JSONField(default=dict)
    intc = models.JSONField(default=dict)
    ibm = models.JSONField(default=dict)

class TransactionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    balance = models.DecimalField(decimal_places=2, default=10000, max_digits=9)

    def save(self, *args, **kwargs):
        self.transaction_date = timezone.now()
        super().save(*args, **kwargs)