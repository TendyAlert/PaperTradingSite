from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render 
from .models import Stock, YFinanceData, UserBalance
from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder 
from django.http import JsonResponse
import json


def stock_portfolio_api_view(request):
    if request.method == 'GET':
        stock_portfolio = Stock.objects.filter(user=request.user)

        stock_portfolio_data = list(stock_portfolio.values())

        return JsonResponse(stock_portfolio_data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def user_detail_api_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_data = {
            'username': user.username,
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    

def create_stock_instance(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            stock_ticker = request.POST.get('stock_ticker')
            bought_at = request.POST.get('cost')
            quantity = request.POST.get('quantity')

            User = get_user_model()
            user = User.objects.get(pk=user_id)

            if not all([user, stock_ticker, bought_at, quantity]):
                return JsonResponse({'error': 'Missing data'}, status=400)

            new_instance = Stock.objects.create(
                user = user,
                stock_ticker = stock_ticker,
                bought_at = bought_at,
                quantity = quantity
            )

            return JsonResponse({'success': True, 'message': 'Stock instance created successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def paperTrading(request):
    stocks = Stock.objects.all()
    data = YFinanceData.objects.all()

    user_balance = UserBalance.objects.filter(user=request.user)
    
    stocks_json = serializers.serialize('json', stocks)
    data_json = serializers.serialize('json', data)

    balance_json = json.dumps(list(user_balance.values('user_id', 'balance')), cls=DjangoJSONEncoder)
    return render(request, "papertrading.html", {'stocks_json': stocks_json, 'data_json': data_json, 'balance_json': balance_json})
