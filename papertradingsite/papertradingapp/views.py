from django.contrib.auth.decorators import login_required
from django.shortcuts import render 
from .models import Stock, YFinanceData, UserBalance
from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder 
from django.http import JsonResponse
import json


def user_detail_api_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_data = {
            'username': user.username,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@login_required
def paperTrading(request):
    stocks = Stock.objects.all()
    data = YFinanceData.objects.all()

    user_balance = UserBalance.objects.filter(user=request.user)
    
    stocks_json = serializers.serialize('json', stocks)
    data_json = serializers.serialize('json', data)

    balance_json = json.dumps(list(user_balance.values('user_id', 'balance')), cls=DjangoJSONEncoder)
    return render(request, "papertrading.html", {'stocks_json': stocks_json, 'data_json': data_json, 'balance_json': balance_json})
