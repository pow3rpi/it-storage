from celery import Celery

from src.entrypoints.container import AppContainer


def create_app() -> Celery:
    container = AppContainer()
    config = container.config()

    application = Celery(config['CELERY']['CELERY_NAME'])
    application.conf.broker_url = config['CELERY']['CELERY_BROKER_URL']
    application.conf.result_backend = config['CELERY']['CELERY_RESULT_BACKEND']

    # email tasks
    application.register_task(container.sign_up_notify_task())
    application.register_task(container.success_sign_up_notify_task())
    application.register_task(container.change_pwd_notify_task())

    return application


app = create_app()
