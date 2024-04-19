from django.shortcuts import render # type: ignore
from .models import Stock, YFinanceData
from django.core import serializers # type: ignore

def paperTrading(request):
    stocks = Stock.objects.all()
    data = YFinanceData.objects.all()
    stocks_json = serializers.serialize('json', stocks)
    data_json = serializers.serialize('json', data)
    return render(request, "papertrading.html", {'stocks_json': stocks_json, 'data_json':data_json})
