from __future__ import absolute_import

from typing import List

import requests
from fastapi.encoders import jsonable_encoder
from sendgrid import sendgrid, Email, To, Content, Mail

import config.settings
from celery_worker.celery import app
from models.model_alert import Alert
from utils import deps

sg = sendgrid.SendGridAPIClient(api_key=config.settings.SENDGRID_API_KEY)


def get_current_btc_price() -> float:
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1' \
          '&sparkline=false'

    resp = requests.get(url)
    data = resp.json()

    return float(data[0]['current_price'])


def send_email(email: str, msg: str):
    from_email = Email(config.settings.SENDGRID_SENDER_EMAIL)
    to_email = To(email)
    subject = 'Price Alert!'
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)
    sg.client.mail.send.post(request_body=mail.get())


@app.task
def alert_mon():
    db = next(deps.get_db())
    offset = 0
    limit = 100

    while True:
        current_price = get_current_btc_price()

        alert_count = db.query(Alert).count()
        alerts: List[dict] = jsonable_encoder(db.query(Alert).offset(offset).limit(limit))
        offset += limit

        if offset > alert_count:
            offset = 0

        for alert in alerts:
            if alert['price'] > current_price:
                send_email(alert['user_email'], 'BTC Price has exceeded {}'.format(alert['price']))
