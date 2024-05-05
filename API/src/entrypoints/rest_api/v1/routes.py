from fastapi import APIRouter

from src.entrypoints.rest_api.v1.handlers import user, link, tutorial, post

app_routes_v1 = APIRouter(prefix='/api/v1')

app_routes_v1.include_router(user.auth_router)
app_routes_v1.include_router(link.router)
app_routes_v1.include_router(tutorial.router)
app_routes_v1.include_router(post.router)
