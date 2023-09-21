import os
import logging_config
import logging

import requests
from dotenv import load_dotenv


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    load_dotenv()
    devman_api_token = os.environ["DEVMAN_API_TOKEN"]
    url = "https://dvmn.org/api/long_polling/"
    headers = {
        'Authorization': f"Token {devman_api_token}"
    }
    timestamp=0
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
            print(response.json())
            timestamp = response.json()["new_attempts"][0]["timestamp"]
            
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError
        ) as exception:
            logger.error("Failed request %s", exception)
            # timestamp = response.json()["timestamp_to_request"]
        print(timestamp)
        # for message in response:
        #     bot.answer(message)