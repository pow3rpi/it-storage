from celery import Celery


class CeleryClient:

    @staticmethod
    def _build_app(name: str, broker_url: str, result_backend: str):
        celery_app = Celery(name)
        celery_app.conf.broker_url = broker_url
        celery_app.conf.result_backend = result_backend
        return celery_app

    def __init__(self, name: str, broker_url: str, result_backend: str):
        self.celery_app = self._build_app(name, broker_url, result_backend)
