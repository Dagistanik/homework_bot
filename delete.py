import requests
from pprint import pprint 

PRACTICUM_TOKEN = 'AQAAAAAjbMawAAYckYJR4oyEAkx2ppgi3upgl38' # Токен Yandex, давался в конце теории
payload = {'from_date': 1635724800}

HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
response = requests.get(url, headers=HEADERS, params=payload).json()
pprint(response)
# zhopa = response['homeworks'][0]['status']
# if zhopa == 'approved':
#     print('лох')