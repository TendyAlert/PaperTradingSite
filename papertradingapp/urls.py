from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path("", views.paperTrading, name='paperTrading'),
    path("transaction_history/", views.transactionHistory, name="transaction_history")
]