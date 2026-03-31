import requests
import json
from datetime import datetime

PROJECT_ID = 'iraq-usd'
API_KEY = 'AIzaSyAHeeAcM3fS6SdL3NNZpAZdfLS8V0N59o4'

def get_dollar_price():
    try:
        response = requests.get('https://liranews.info/currencies/usdiqd', 
                              headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            import re
            match = re.search(r'(\d{1,3}(?:,\d{3})+(?:\.\d+)?)\s*د\.ع', response.text)
            if match:
                price_text = match.group(1).replace(',', '')
                price = float(price_text)
                if price < 1000:
                    price = price * 100
                return int(price)
    except:
        pass
    
    return 146000

def update_firebase(price):
    url = f'https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/usd_prices/current?key={API_KEY}'
    
    data = {
        'fields': {
            'value': {'integerValue': str(price)},
            'updatedAt': {'timestampValue': datetime.utcnow().isoformat() + 'Z'}
        }
    }
    
    response = requests.patch(url, json=data)
    print(f'Updated: {price} - Status: {response.status_code}')

if __name__ == '__main__':
    price = get_dollar_price()
    update_firebase(price)
