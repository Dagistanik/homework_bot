import requests
from pprint import pprint 
from dotenv import load_dotenv
import os
import exceptions


# PRACTICUM_TOKEN = 'AQAAAAAjbMawAAYckYJR4oyEAkx2ppgi3upgl38' # Токен Yandex, давался в конце теории
# payload = {'from_date': 1635724800}

# HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
# url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
# response = requests.get(url, headers=HEADERS, params=payload).json()
# response = response['homeworks']
# pprint(response)
# # zhopa = response['homeworks'][0]['status']
# # if zhopa == 'approved':
# #     print('лох')




load_dotenv()

# def check_tokens():
#     """Проверяет доступность переменных окружения"""
#     # if os.environ.get('PRACTICUM_TOKEN','TELEGRAM_TOKEN','TELEGRAM_CHAT_ID') == True:
#     if 'PRACTICUM_TOKEN' and 'TELEGRAM_TOKEN' and 'TELEGRAM_CHAT_ID' in os.environ:
#         return True
#     else:
#     # elif os.getenv('PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID') is not None:
#         return False

# def check_tokens():
#     """Проверяет доступность переменных окружения"""

#     itog = os.environ.get('PRACTICUM_TOKEN')
#     if itog != None:
#         print(itog)
#         itog = os.environ.get('TELEGRAM_TOKEN')
#         if itog != None:
#             print(itog)
#             itog = os.environ.get('TELEGRAM_CHAT_ID')
#             if itog != None:
#                 print(itog)
#                 return True
                
#     else:
#         print('pol')
        
# check_tokens()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') 

def check_tokens():
    """Проверяет доступность переменных окружения"""
    if PRACTICUM_TOKEN is None:
        if TELEGRAM_TOKEN is None:
            if TELEGRAM_CHAT_ID is None:
                return True
    else:
        return False
    
check_tokens()
