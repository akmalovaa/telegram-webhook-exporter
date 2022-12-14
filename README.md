# Telegram Webhook info exporter

This is a very simple Prometheus exporter for Telegram Bot API [getWebhookInfo](https://core.telegram.org/bots/api#webhookinfo) to check the work of the telegram bot via webhook


Used JSON info GET URL - https://api.telegram.org/YOUR_TOKEN/getWebhookInfo

Prometheus Metrics:
- **tg_pending_update_count** - pending_update_count Number of updates awaiting delivery (required 0)
- **tg_check_error** - Check last_error_message > True: 1 False: 0 (required 0)
- **tg_check_ip** - Check ip address > True: 1 False: 0 (Optional: required 1)
- **tg_check_url** - Check URL address > True: 1 False: 0 (Optional: required 1)

## Installation


### Docker build

```bash
git clone https://github.com/akmalovaa/telegram-webhook-exporter.git
cd telegram-webhook-exporter
docker build . -t telegram_webhook_exporter
cp .env.example .env
```
```bash
nano .env
```
Change file .env
Edit YOUR TOKEN and UPDATE PERIOD

Run:

```bash
docker-compose up -d
```
or using docker run an environment variable:

```bash
$ docker run \
  -e 'TOKEN=<your bot token>' \
  -e 'UPDATE_PERIOD=15' \
  -e 'PORT=8000' \
  -p 8000:8000 \
  telegram_webhook_exporter
```

## Grafana
Example used type - State timeline

![telegram-webhook-exporter](https://github.com/akmalovaa/telegram-webhook-exporter/blob/master/telegram-webhook-exporter.png)



## License

telegram-webhook-exporter is released under the [MIT license](LICENSE).
