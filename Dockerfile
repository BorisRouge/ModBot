FROM python:3.9-slim

WORKDIR /home/ModBot
COPY . /home/ChatGPTbot
RUN pip install -r requirements.txt


# указать переменные окружения здесь или при запуске контейнера
ENV ADMIN_ID
ENV TELEGRAM_BOT_TOKEN
RULES_FILENAME=rules.py
RULES_PATH=utils/rules.py

ENTRYPOINT python start.py