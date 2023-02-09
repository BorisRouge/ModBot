FROM python:3.9-slim

WORKDIR /home/ModBot
COPY . /home/ModBot
ENV PYTHONPATH /home/ModBot
RUN pip install -r requirements.txt


# указать переменные окружения здесь или при запуске контейнера

ENV RULES_FILENAME='rules.py'
ENV RULES_PATH='utils/rules.py'

ENTRYPOINT python start.py