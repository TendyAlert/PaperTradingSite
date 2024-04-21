from django.contrib import admin #type: ignore
from .models import Stock, YFinanceData, UserBalance, TransactionHistory

# Register your models here.
admin.site.register(UserBalance)
admin.site.register(Stock)
admin.site.register(YFinanceData)
admin.site.register(TransactionHistory)