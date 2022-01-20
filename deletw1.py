import requests
import os 
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

PRACTICUM_ENDPOINT = ('https://practicum.yandex.ru/api/user_api/'
    'homework_statuses/')
PRACTICUM_HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

params = {'from_date': 0}
response = requests.get(
            PRACTICUM_ENDPOINT, headers=PRACTICUM_HEADERS, params=params).json()
if not isinstance(response, dict):
    pprint('zhopa')
zhopa = response.get('homeworks')
if isinstance(zhopa, list):
        pprint('ne_zhopa')