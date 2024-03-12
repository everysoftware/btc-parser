import datetime

import requests
from celery import Celery
from celery.schedules import crontab

from src.config import settings

app = Celery("tasks", broker=settings.redis_url, backend=settings.redis_url)


@app.task
def load_dump() -> int:
    """Загрузка дампа транзакций с Blockchair за предыдущий день."""
    date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    # date = "2009-01-12"

    result = requests.post(
        f"http://localhost:8000/load_dump?date={date}",
    )

    return result.status_code


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **_kwargs):
    """Настройка периодической задачи для загрузки дампа транзакций."""
    sender.add_periodic_task(
        # Каждый день в 00:15 (UTC)
        crontab(hour="0", minute="15"),
        load_dump.s(),
    )
