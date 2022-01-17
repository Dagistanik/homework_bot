from pprint import pprint

import requests 

response = requests.get('https://api.telegram.org/bot5034309692:AAEQ8naVkd5wHkLRm0CoIFV8rWNGGQMPYP0/getUpdates')
pprint(response.json())

# response = requests.get('https://api.telegram.org/bot5034309692:AAEQ8naVkd5wHkLRm0CoIFV8rWNGGQMPYP0/sendMessage?chat_id=389706145&text=мне не верь,я бот, нужно верить Богу')