from django.contrib import admin #type: ignore
from .models import Stock

# Register your models here.
admin.site.register(Stock)