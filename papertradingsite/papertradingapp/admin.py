from django.contrib import admin #type: ignore
from .models import UserBalance, Stock

# Register your models here.
admin.site.register(UserBalance)
admin.site.register(Stock)