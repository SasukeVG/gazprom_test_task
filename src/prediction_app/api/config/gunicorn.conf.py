import os
import signal

from prediction_app.api.config.sgi_config import sgi_config

wsgi_app = sgi_config.WSGI_APP
bind = f"{sgi_config.HOST}:{sgi_config.PORT}"
workers = sgi_config.WORKERS_COUNT
worker_class = sgi_config.WORKER_CLASS
reload = sgi_config.AUTO_RELOAD
# loglevel = sgi_config.LOG_LEVEL
# accesslog = sgi_config.ACCESS_LOG


def worker_int(worker):
    """
    Метод необходим для корректного релоада gunicorn
    """
    os.kill(worker.pid, signal.SIGINT)
