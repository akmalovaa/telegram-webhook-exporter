import time
import requests
import json
import os
import sys
import logging

from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge, Info

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
UPDATE_PERIOD = int(os.getenv('UPDATE_PERIOD'))
TOKEN = os.getenv('TOKEN')
URL = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"

#Create a metric to track time spent and requests made.
TG_PENDING_UPDATE_COUNT = Gauge('tg_pending_update_count', 'Number of updates awaiting delivery')
TG_CHECK_ERROR = Gauge('tg_check_error', 'Checking last error message - True : 1 or False : 0')
TG_CHECK_IP = Gauge('tg_check_ip', 'Checking IP address - True : 1 or False : 0')
TG_CHECK_URL = Gauge('tg_check_url', 'Checking URL - True : 1 or False : 0')


def getWebhookInfo() -> dict:
    try:
        response = requests.get(URL)
    except Exception as err:
        logging.info(f'Response error: {err}')
        return {}
    else:
        return response.json()


def telegram_response_pars():
    data: dict = getWebhookInfo()
    logging.info(f"Webhook result: {data}")
    pending_update_count: int = data.get('result', {}).get('pending_update_count', 2)
    ip_address: str = data.get('result', {}).get('ip_address', 'None')
    webhook_url: str = data.get('result', {}).get('url', 'None')
    last_error_message: str = data.get('result', {}).get('last_error_message', 'None')
    last_error_date: int | str = data.get('result', {}).get('last_error_date', 'None')

    TG_PENDING_UPDATE_COUNT.set(pending_update_count)
    TG_CHECK_IP.set('0') if ip_address == 'None' else TG_CHECK_IP.set('1')
    TG_CHECK_URL.set('0') if webhook_url == 'None' or webhook_url == '' else TG_CHECK_URL.set('1')
    TG_CHECK_ERROR.set('0') if last_error_message == 'None' else TG_CHECK_ERROR.set('1')


if __name__ == '__main__':
    start_http_server(8000)
    while True:
        telegram_response_pars()
        time.sleep(UPDATE_PERIOD)
