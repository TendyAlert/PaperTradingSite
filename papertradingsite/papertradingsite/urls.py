"""
URL configuration for papertradingsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import include, path # type: ignore
from papertradingapp import views

urlpatterns = [
    path('papertrading/', include("papertradingapp.urls")),
    path('api/user/<int:user_id>/', views.user_detail_api_view, name='user_detail_api'),
    path('api/user_balance/<int:user_id>/', views.update_user_balance_api_view, name='update_user_balance_api'),
    path('api/stock_portfolio/', views.stock_portfolio_api_view, name='stock_protfolio_api'),
    path('create_stock_instance/', views.create_stock_instance, name='create_stock_instance'),
    path('remove_stock_instance/', views.remove_stock_instance, name='remove_stock_instance'),
    path('delete_all_stocks/<int:user_id>/', views.delete_all_stocks, name='delete_all_stocks'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]
