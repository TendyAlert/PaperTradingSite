from django.core.management.base import BaseCommand #type: ignore
from papertradingapp.models import YFinanceData, Stock
import yfinance as yf #type: ignore
from datetime import datetime, timedelta
import json

class Command(BaseCommand):
    help = 'Populates the YFinanceData model with default data'

    def handle(self, *args, **kwargs):
        # Get data for each stock ticker
        date_four_months_ago = datetime.now() - timedelta(weeks=13)
        aapl_data = yf.Ticker('AAPL').history(start=date_four_months_ago, end = datetime.now(), interval='1d')
        amd_data = yf.Ticker('AMD').history(start=date_four_months_ago, end = datetime.now(), interval='1d')
        intc_data = yf.Ticker('INTC').history(start=date_four_months_ago, end = datetime.now(), interval='1d')
        ibm_data = yf.Ticker('IBM').history(start=date_four_months_ago, end = datetime.now(), interval='1d')

        # Save the data in the database
        YFinanceData.objects.create(
            aapl=json.dumps(aapl_data.to_json()), 
            amd=json.dumps(amd_data.to_json()), 
            intc=json.dumps(intc_data.to_json()),
            ibm=json.dumps(ibm_data.to_json())
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated YFinanceData with stock data'))