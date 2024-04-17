from django.contrib import admin
from .models import UserBalance, Portfolio

# Register your models here.
admin.site.register(UserBalance)
admin.site.register(Portfolio)