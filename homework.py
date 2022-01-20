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
PRACTICUM_ENDPOINT = ('https://practicum.yandex.ru/api/user_api/'
                      'homework_statuses/')

PRACTICUM_HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

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
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception:
        logger.error('Ошибка при отправке сообщения')
        raise exceptions.Erbot


def get_api_answer(current_timestamp):
    """Делает запрос к API серверу."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            PRACTICUM_ENDPOINT, headers=PRACTICUM_HEADERS, params=params)
        if response.status_code == HTTPStatus.OK:
            return response.json()
        raise exceptions.Erbot('статус код не равен 200')
    except requests.RequestException as error:
        inf = f'Недоступен путь:{error}'
        logger.error(inf)
        raise exceptions.Erbot(inf)


def check_response(response):
    """Проверка ответа API на корректность."""
    if not isinstance(response, dict):
        raise TypeError('response не является словарем')
    if 'homeworks' not in response:
        raise KeyError('ключа homework нет в response')
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise KeyError()
    return homeworks


def parse_status(homework):
    """Извлекает статус конкретной домашней работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if not homework_status:
        raise KeyError('в домашней работе нет homework_status')
    if not homework_name:
        raise KeyError('в домашней работе нет homework_name')
    if homework_status in HOMEWORK_STATUSES:
        verdict = HOMEWORK_STATUSES.get(homework_status)
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    error = 'Нет таких статусов'
    logger.error(error)
    raise KeyError(error)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if all([TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, PRACTICUM_TOKEN]):
        return True
    inf = 'Переменные телеграма недоступны:'
    logger.critical(inf)
    return False


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    result = []
    while True:
        try:
            response = get_api_answer(current_timestamp)
            if not response['homeworks']:
                continue
            homework = check_response(response)[0]
            if homework['status'] != result:
                message = parse_status(homework)
                send_message(bot, message)
                logger.info('Сообщение отправлено')
            else:
                logger.debug('Статус не изменился')
            result = homework['status']
            current_timestamp = response['current_date']
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
