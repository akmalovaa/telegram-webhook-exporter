import sys
import logging
import time
import datetime

import envcast
import requests
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge, metrics


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(message)s')

UPDATE_PERIOD: int = envcast.env("UPDATE_PERIOD", 15, type_cast=int)
TOKEN: str = envcast.env("TOKEN", "", type_cast=str)
if not TOKEN:
    raise ValueError("Missing telegram token in enviroment variables")
URL: str = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
PORT: int = envcast.env("PORT", 8000, type_cast=int)

#Create a metric to track time spent and requests made.
TG_PENDING_UPDATE_COUNT: metrics.Gauge = Gauge('tg_pending_update_count', 'Number of updates awaiting delivery')
TG_CHECK_ERROR: metrics.Gauge = Gauge('tg_check_error', 'Checking last error message - True : 1 or False : 0')
TG_CHECK_IP: metrics.Gauge = Gauge('tg_check_ip', 'Checking IP address - True : 1 or False : 0')
TG_CHECK_URL: metrics.Gauge = Gauge('tg_check_url', 'Checking URL - True : 1 or False : 0')


def fetch_webhook_info() -> dict:
    try:
        response = requests.get(URL)
        return response.json()
    except Exception as err:
        logging.info(f'Response error: {err}')
        return {}


def parse_telegram_response() -> None:
    webhook_info: dict = fetch_webhook_info()
    logging.info(f"Webhook result: {webhook_info}")
    pending_update_count: int = webhook_info.get("result", {}).get("pending_update_count", 1)
    ip_address: str | None = webhook_info.get("result", {}).get("ip_address")
    webhook_url: str | None = webhook_info.get("result", {}).get("url")
    last_error_message: str | None = webhook_info.get("result", {}).get("last_error_message")
    last_error_date: str | None = webhook_info.get("result", {}).get("last_error_date")
    # no checking the last error more than 60 seconds ago
    last_error_time: datetime.datetime = datetime.datetime.utcfromtimestamp(int(last_error_date))
    now_time: datetime.datetime = datetime.datetime.now()
    sec_after_last_error: float = (now_time - last_error_time).total_seconds()

    TG_PENDING_UPDATE_COUNT.set(pending_update_count)
    TG_CHECK_ERROR.set(0 if last_error_message is None or sec_after_last_error > 60 else 1)
    TG_CHECK_IP.set(0 if ip_address is None else 1)
    TG_CHECK_URL.set(0 if webhook_url is None or webhook_url ==''  else 1)


def start_export_cycle() -> None:
    while True:
        parse_telegram_response()
        time.sleep(UPDATE_PERIOD)


if __name__ == '__main__':
    start_http_server(PORT)
    logging.info(f'Server prometheus telegram exporter up localhost:{PORT}')
    start_export_cycle()
