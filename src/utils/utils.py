import os
import time
import requests


def sendMessage(message):
    data = {"text": message}
    url = os.getenv('SLACK_WEBHOOK_URL')
    requests.post(url, json=data)


def log(message, filename="./data/sell-log.csv"):
    timestamp = int(round(time.time()))
    f = open(filename, "a+")
    f.write(str(timestamp) + ',' + message)
    f.close()


def sleep(seconds):
    time.sleep(seconds)
