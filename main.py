import os
import logging
import logging.config
from time import sleep

import requests
from dotenv import load_dotenv

import telegram


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    "loggers": {"": {"handlers": ['file'], "level": "DEBUG"}},
}


logger = logging.getLogger(__name__)


def create_message(attempt_details):
    positive_message = "Преподавателю всё понравилось, \
        можно приступать к следущему уроку!"
    negative_message = "К сожалению, в работе нашлись ошибки."
    message = negative_message if attempt_details["is_negative"] \
        else positive_message
    template = 'У вас проверили работу "{title}"\n\n{link}\n\n{message}'
    email_message = template.format(
        title=attempt_details["lesson_title"],
        link=attempt_details["lesson_url"],
        message=message
    )
    return email_message


if __name__ == "__main__":
    load_dotenv()
    logging.config.dictConfig(LOGGING)
    url = "https://dvmn.org/api/long_polling/"
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    devman_api_token = os.environ["DEVMAN_API_TOKEN"]
    headers = {'Authorization': f"Token {devman_api_token}"}
    timestamp = ""
    params = {}
    bot = telegram.Bot(token=tg_token)
    while True:
        try:
            if timestamp:
                params["timestamp"] = timestamp
            response = requests.get(
                url,
                headers=headers,
                timeout=60,
                params=params,
            )
            response.raise_for_status()
            dvmn_answer = response.json()
            logger.info(dvmn_answer)
            if dvmn_answer['status'] == 'timeout':
                timestamp = dvmn_answer['timestamp_to_request']
            else:
                attempt_details = dvmn_answer["new_attempts"][0]
            message = create_message(attempt_details)
            timestamp = attempt_details["timestamp"]
            bot.send_message(chat_id=chat_id, text=message)
        except requests.exceptions.ReadTimeout as exception:
            logger.error("Failed request %s", exception)
        except requests.exceptions.ConnectionError:
            logging.error('No network connection!')
            sleep(6)
