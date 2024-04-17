from django.shortcuts import render # type: ignore
from django.http import JsonResponse # type: ignore
from django.core import serializers # type: ignore
from .models import UserBalance


def paperTrading(request):
    userBalance = UserBalance.objects.all()
    sterialized_data = serializers.serialize('json', userBalance)
    return JsonResponse(sterialized_data, safe=False)
