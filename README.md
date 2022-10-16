# Telegram Webhook info exporter

This is a Prometheus exporter for Telegram Bot API getWebhookInfo.
Simple Python exporter

Used JSON info GET URL - https://api.telegram.org/YOUR_TOKEN/getWebhookInfo

## Installation


### Docker build

```bash
git clone https://github.com/akmalovaa/telegram-webhook-exporter.git
cd telegram-webhook-exporter
docker build . -t telegram_webhook_exporter
cp .env.example .env
```

Change file .env
Edit YOUR TOKEN and UPDATE PERIOD

```bash
docker-compose up -d
```
or using docker run an environment variable:

```bash
$ docker run \
  -e 'TOKEN=<your bot token>', 'UPDATE_PERIOD=15' \
  -p 8000:8000 \
  telegram_webhook_exporter
```



## License

telegram-webhook-exporter is released under the [MIT license](LICENSE).
