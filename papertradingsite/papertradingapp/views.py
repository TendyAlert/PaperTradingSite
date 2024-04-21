from django.contrib.auth.decorators import login_required
from django.shortcuts import render 
from .models import Stock, YFinanceData, UserBalance, TransactionHistory
from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder 
from django.http import JsonResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
import json


def delete_all_stocks(request, user_id):
    if request.method =="DELETE":
        try:
            user = User.objects.get(pk = user_id)
            default_balance = 10000
            stocks = Stock.objects.filter(user = user)
            stocks.delete()

            transactionHistory = TransactionHistory.objects.filter(user_id = user_id)
            transactionHistory.delete()
            transactionHistory.create(
                user = user,
                balance = default_balance
            )

            return JsonResponse({'success': True, 'message': "Stocks removed succesfully"})
        except Stock.DoesNotExist:
            return JsonResponse({'error': 'Stock not found'}, status=404)

def update_user_balance_api_view(request, user_id):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            new_balance = data.get('balance')
            new_balance = round(float(new_balance), 2)

            user_balance = UserBalance.objects.get(user_id = user_id)
            user_balance.balance = new_balance
            user_balance.save()

            transaction = TransactionHistory.objects.create(
                user=user_balance.user,
                balance=new_balance
            )

            return JsonResponse({
                'success': True, 
                'message': 'User balance updated successfully', 
                'new_balance':user_balance.balance,
                'transaction_id': transaction.id})
        except UserBalance.DoesNotExist:
            return JsonResponse({'error': 'User balance not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except UserBalance.DoesNotExist:
            return JsonResponse({'error': 'User balance not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


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

            user = request.user

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

def remove_stock_instance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stock_ticker = data.get('stock_ticker')
            amount_sold = int(data.get('amount'))

            stock_instance = Stock.objects.filter(user=request.user, stock_ticker=stock_ticker.upper()).first()

            if stock_instance:
                if stock_instance.quantity >= amount_sold:
                    if stock_instance.quantity == amount_sold:
                        stock_instance.delete()
                    else:
                        stock_instance.quantity -= amount_sold
                        stock_instance.save()
                    
                    return JsonResponse({'success': True, 'message': 'Stock instance removed successfully'})
                else:
                    return JsonResponse({'error': 'Not enough stocks to sell'}, status=400)
            else:
                return JsonResponse({'error': 'Stock not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def paperTrading(request):
    stocks = Stock.objects.all()
    data = YFinanceData.objects.all()

    user_balance = UserBalance.objects.filter(user=request.user)
    
    stocks_json = serializers.serialize('json', stocks)
    data_json = serializers.serialize('json', data)

    balance_json = json.dumps(list(user_balance.values('user_id', 'balance')), cls=DjangoJSONEncoder)
    return render(request, "papertrading.html", {'stocks_json': stocks_json, 'data_json': data_json, 'balance_json': balance_json})

def transactionHistory(request):

    user_transactions = TransactionHistory.objects.filter(user = request.user)
    transaction_json = serializers.serialize('json', user_transactions)

    return render(request, "transactionhistory.html", {'transaction_json': transaction_json})

@receiver(post_save, sender=User)
def create_transaction_history(sender, instance, created, **kwargs):
    if created:
        TransactionHistory.objects.create(user=instance, balance=10000)
