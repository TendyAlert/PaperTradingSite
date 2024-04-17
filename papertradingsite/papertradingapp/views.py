from django.shortcuts import render # type: ignore
from .models import UserBalance
from django.core import serializers # type: ignore

def paperTrading(request):
    userBalances = UserBalance.objects.all()
    userBalances_json = serializers.serialize('json', userBalances)
    return render(request, "papertrading.html", {'userBalances_json': userBalances_json})
