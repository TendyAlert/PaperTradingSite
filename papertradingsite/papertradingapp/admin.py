from django.contrib import admin #type: ignore
from .models import Stock, YFinanceData

# Register your models here.
admin.site.register(Stock)
admin.site.register(YFinanceData)