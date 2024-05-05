from fastapi import APIRouter

from src.entrypoints.rest_api.v1.routes import app_routes_v1

app_routes = APIRouter()

app_routes.include_router(app_routes_v1)
