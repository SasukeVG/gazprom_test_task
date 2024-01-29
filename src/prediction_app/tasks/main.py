import celery_decorator_taskcls
# celery_pool_asyncio importing is optional
# It imports when you run worker or beat if you define pool or scheduler
# but it does not imports when you open REPL or when you run web application.
# If you want to apply monkey patches anyway to make identical environment
# when you use REPL or run web application app it's good idea to import
# celery_pool_asyncio module
import celery_pool_asyncio  # noqa
from celery import Celery


# Sometimes noqa does not disable linter (Spyder IDE)
celery_pool_asyncio.__package__

celery_decorator_taskcls.patch_celery()

from prediction_app.tasks.config.celery import celery_config

celery_app = Celery(
    __name__,
    broker=celery_config.BROKER_URL,
    backend=celery_config.BACKEND_URL,
    worker_pool='celery_pool_asyncio:TaskPool'
)

celery_app.autodiscover_tasks(["prediction_app.tasks.task"])

# celery_app.conf.update({
#     'worker_pool': 'celery_pool_asyncio:TaskPool'
# })
