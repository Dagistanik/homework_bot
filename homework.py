import os
import logging
import requests
import time
from dotenv import load_dotenv
import exception
import telegram
...

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID') 

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    logging.info('Сообщение отправлено')
    bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=message
    )


def get_api_answer(current_timestamp):
    """Делает запрос к API серверу"""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    try:
        if response.status_code == 200:
            response = requests.get(ENDPOINT, headers=HEADERS, params=params).json()
            return response
        else:
            raise exception.Erbot('статус код не равен 200')
    except exception.Erbot as error:
        inf = f'Недоступен путь:{error}'
        logging.error(inf)

  


def check_response(response):
    """Проверка ответа API на корректность"""
    if type(response) == dict:
        response['current_date']
        homeworks = response['homeworks']
        if type(homeworks) == list:
            return homeworks
    raise exception.Erbot('Переменная response  не является словарём')


def parse_status(homework):
    """Извлекает статус конкретной домашней работы"""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_status in HOMEWORK_STATUSES:
        verdict = HOMEWORK_STATUSES.get(homework_status)
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    raise exception.Erbot('Нет таких статусов')

def check_tokens():
    """Проверяет доступность переменных окружения"""
    if 'PRACTICUM_TOKEN' and 'TELEGRAM_TOKEN' and 'TELEGRAM_CHAT_ID' in os.environ:
        return True
    else:
        return False

def main():
    """Основная логика работы бота."""
    ...

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    ...

    while True:
        try:
            response = get_api_answer(current_timestamp)
            if response.get('homeworks'):
                send_message(bot, parse_status(response.get('homeworks')[0]))
            current_timestamp = response.get('current_date', current_timestamp)
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            time.sleep(RETRY_TIME)
        else:
            ...


if __name__ == '__main__':
    main()
