import os
import logging

import requests
from dotenv import load_dotenv

import telegram


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    load_dotenv()
    tg_token = os.environ["TG_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    bot = telegram.Bot(token=tg_token)

    devman_api_token = os.environ["DEVMAN_API_TOKEN"]
    url = "https://dvmn.org/api/long_polling/"
    headers = {
        'Authorization': f"Token {devman_api_token}"
    }
    timestamp = ""
    positive_message = "Преподавателю всё понравилось, \
        можно приступать к следущему уроку!"
    negative_message = "К сожалению, в работе нашлись ошибки."
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
            message = negative_message if attempt_details["is_negative"] else positive_message
            timestamp = attempt_details["timestamp"]
            answer = """У вас проверили работу "{}"
{}

{}""".format(attempt_details["lesson_title"], attempt_details["lesson_url"], message)
            bot.send_message(chat_id=chat_id, text=answer)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout
        ) as exception:
            logger.error("Failed request %s", exception)
