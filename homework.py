import os
import logging
import requests
import time
import exceptions
import telegram
from dotenv import load_dotenv
from http import HTTPStatus

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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    if bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message):
        True
    else:
        logger.error('Ошибка при отправке сообщения')
        raise exceptions.Erbot


def get_api_answer(current_timestamp):
    """Делает запрос к API серверу."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    try:
        if response.status_code == HTTPStatus.OK:
            response = requests.get(
                ENDPOINT, headers=HEADERS, params=params).json()
            return response
        else:
            raise exceptions.Erbot('статус код не равен 200')
    except exceptions.Erbot as error:
        inf = f'Недоступен путь:{error}'
        logger.error(inf)
        raise exceptions.Erbot(inf)


def check_response(response):
    """Проверка ответа API на корректность."""
    if type(response) == dict:
        response['current_date']
        homeworks = response['homeworks']
        if type(homeworks) == list:
            return homeworks
        else:
            error = 'переменная homeworks не список'
            logger.error(error)
            raise TypeError(error)
    else:
        error = 'Переменная response  не является словарём'
        logger.error(error)
        raise TypeError(error)


def parse_status(homework):
    """Извлекает статус конкретной домашней работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if not homework_status:
        raise KeyError
    if not homework_name:
        raise KeyError
    if homework_status in HOMEWORK_STATUSES:
        verdict = HOMEWORK_STATUSES.get(homework_status)
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    raise KeyError('Нет таких статусов')


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if TELEGRAM_TOKEN is not None or TELEGRAM_CHAT_ID is not None:
        if PRACTICUM_TOKEN is not None:
            return True
        else:
            inf = 'Переменная PRACTICUM_TOKEN недоступна:'
            logger.error(inf)
            return False
    else:
        inf = 'Переменные телеграма недоступны:'
        logger.critical(inf)
        return False


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    result = []
    while True:
        try:
            response = get_api_answer(current_timestamp)
            if response['homeworks']:
                homework = check_response(response)[0]
                if homework['status'] != result:
                    message = parse_status(homework)
                    send_message(bot, message)
                    logger.info('Сообщение отправлено')
                else:
                    logger.debug('Статус не изменился')
                result = homework['status']
            current_timestamp = response['current_date']
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            time.sleep(RETRY_TIME)
        else:
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
