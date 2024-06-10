# devman-bot
 
Telegram bot for sending notifications about verification of works on [dvmn.org](https://dvmn.org/modules).

## How to install

```
pip install -r requirements.txt
```

* **Run on local machine**

To get started you need:

Get a token from [dvmn.org](https://dvmn.org/api/docs/)
Then create a bot in TG [(How to create a channel, a bot and get a token.)](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)
Find out your id in telegram (you can find out by writing to the bot [@userinfobot](https://t.me/userinfobot))

Create .env file with environment variables:
```
DEVMAN_API_TOKEN=<TOKEN_DEVMAN>
TG_TOKEN=<TOKEN_BOT>
TG_CHAT_ID=<CHAT_ID>
```

## Usage
```
python main.py
```

# Running with Docker
- Register on the site and download [Docker](https://www.docker.com/)
- Run the image creation command `docker build --tag dvmn-bot-docker .`
- Click the Run button in Docker Desktop, set the environment variables and run the image.
- Or run the container using the command `docker run -d --env-file.env dvmn-bot-docker`