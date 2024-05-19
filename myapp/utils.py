import requests
from .models import CryptoData
from datetime import datetime

def Fetch_And_UpdateCryptoData(api_key):

    ApiUrl = f'https://api.example.com/crypto_data?apikey=d77eb42187b3622a83f1bba9fb267e6053dfa18f25c1c652a2cba6a3e107b5d0'

    try:
        response = requests.get(ApiUrl)
        data = response.json()
        current_timestamp = datetime.now()

        # Parse and update the database with the real-time data
        for symbol, values in data.items():
            open_price = values.get('open_price')
            high_price = values.get('high_price')
            low_price = values.get('low_price')
            close_price = values.get('close_price')

            crypto_data, created = CryptoData.objects.get_or_create(symbol=symbol)

            crypto_data.open_price = open_price
            crypto_data.high_price = high_price
            crypto_data.low_price = low_price
            crypto_data.close_price = close_price
            crypto_data.timestamp = current_timestamp


            crypto_data.save()



    except Exception as e:
        # Handle errors (e.g., network issues, API rate limiting)
        pass
