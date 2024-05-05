from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.entrypoints.container import Container
from src.entrypoints.rest_api.app_routes import app_routes


def create_app():
    container = Container()
    container.wire(modules=[
        'src.entrypoints.rest_api.v1.handlers.user',
        'src.entrypoints.rest_api.v1.handlers.link',
        'src.entrypoints.rest_api.v1.handlers.tutorial',
        'src.entrypoints.rest_api.v1.handlers.post',
    ])
    application = FastAPI(
        title='IT-Storage',
        version='v1',
        docs_url=None,
        redoc_url=None,
    )
    application.include_router(app_routes)
    origins = [
        'http://127.0.0.1:3000',
    ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    return application


app = create_app()
