from django.shortcuts import render # type: ignore
from .models import Stock
from django.core import serializers # type: ignore

def paperTrading(request):
    stocks = Stock.objects.all()
    stocks_json = serializers.serialize('json', stocks)
    return render(request, "papertrading.html", {'stocks_json': stocks_json})
