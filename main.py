import os
import logging
from time import sleep

import requests
from dotenv import load_dotenv

import telegram


logger = logging.getLogger(__name__)


def create_email_message(attempt_details):
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
    url = "https://dvmn.org/api/long_polling/"
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["TG_CHAT_ID"]
    devman_api_token = os.environ["DEVMAN_API_TOKEN"]
    headers = {'Authorization': f"Token {devman_api_token}"}
    timestamp = ""
    bot = telegram.Bot(token=tg_token)
    while True:
        params = {"timestamp": timestamp}
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=60,
                params=params,
            )
            response.raise_for_status()
            query = response.json()
            logger.info(query)
            attempt_details = query["new_attempts"][0]
            email_message = create_email_message(attempt_details)
            timestamp = attempt_details["timestamp"]
            bot.send_message(chat_id=chat_id, text=email_message)
        except requests.exceptions.ReadTimeout as exception:
            logger.error("Failed request %s", exception)
        except requests.exceptions.ConnectionError:
            logging.error('No network connection!')
            sleep(6)
