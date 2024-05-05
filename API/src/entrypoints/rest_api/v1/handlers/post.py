from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.core.enums import SearchEnum, APIHandlerEnum
from src.core.exceptions.user import InvalidToken
from src.entrypoints.core import oauth2_scheme
from src.entrypoints.container import Container
from src.interface.logger import LoggerInterface
from src.interface.services.auth import AuthServiceInterface
from src.schema.post import DeletePostRequest
from src.schema.user import UserVerifyRequest
from src.usecase.blog.post import PostUseCase
from ..config import UnknownErrorException

router = APIRouter(prefix='/posts', tags=['Post'])


@router.get('/tags', summary='Get tags')
@inject
async def get_tags(string: str,
                   use_case: PostUseCase = Depends(Provide[Container.post_use_case]),
                   auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                   tokens: UserVerifyRequest = Depends(oauth2_scheme),
                   logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        await auth_service.get_current_user(tokens.access_token)
        tags = await use_case.get_tags(string)
        return JSONResponse(
            status_code=200,
            content=tags.to_dict()
        )
    except InvalidToken as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.GET_TAGS,
            message=str(error)
        )
        raise UnknownErrorException


@router.get('', summary='Get posts by tags/title')
@inject
async def get_posts(type: SearchEnum,
                    name: str = None,
                    topic: str = None,
                    page: int = 0,
                    use_case: PostUseCase = Depends(Provide[Container.post_use_case]),
                    auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                    tokens: UserVerifyRequest = Depends(oauth2_scheme),
                    logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        posts = await use_case.get_posts(
            user=user,
            search_type=type,
            search_filter=topic.split(',') if topic else name,
            page=page
        )
        return JSONResponse(
            status_code=200,
            content=posts.to_dict()
        )
    except InvalidToken as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.GET_POSTS,
            message=str(error)
        )
        raise UnknownErrorException


@router.delete('/', summary='Delete posts')
@inject
async def delete_post(request_data: DeletePostRequest,
                      use_case: PostUseCase = Depends(Provide[Container.post_use_case]),
                      auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                      tokens: UserVerifyRequest = Depends(oauth2_scheme),
                      logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        await use_case.delete_post(user, request_data)
        return JSONResponse(
            status_code=200,
            content={'message': 'OK'}
        )
    except InvalidToken as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.DELETE_POST,
            message=str(error)
        )
        raise UnknownErrorException
