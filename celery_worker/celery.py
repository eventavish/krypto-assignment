from __future__ import absolute_import
from celery import Celery

import config.settings

app = Celery('celery_worker',
             broker=config.settings.CELERY_BROKER,
             backend='rpc://',
             include=['celery_worker.alert_monitor'])

