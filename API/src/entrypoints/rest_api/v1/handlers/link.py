from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.core.enums import APIHandlerEnum
from src.core.exceptions.blog import ContentNotFound
from src.core.exceptions.user import InvalidToken
from src.entrypoints.container import Container
from src.entrypoints.core import oauth2_scheme
from src.interface.logger import LoggerInterface
from src.interface.services.auth import AuthServiceInterface
from src.schema.link import CreateLinkRequest, UpdateLinkRequest
from src.schema.user import UserVerifyRequest
from src.usecase.blog.link import LinkUseCase
from ..config import UnknownErrorException

router = APIRouter(prefix='/links', tags=['Link'])


@router.post('/create', summary='Create link')
@inject
async def create_link(request_data: CreateLinkRequest,
                      use_case: LinkUseCase = Depends(Provide[Container.link_use_case]),
                      auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                      tokens: UserVerifyRequest = Depends(oauth2_scheme),
                      logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        await use_case.create_link(user, request_data)
        return JSONResponse(
            status_code=201,
            content={'message': 'OK'}
        )
    except InvalidToken as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.CREATE_LINK,
            message=str(error)
        )
        raise UnknownErrorException


@router.get('/{post_id}', summary='Get link')
@inject
async def get_link(post_id: int,
                   use_case: LinkUseCase = Depends(Provide[Container.link_use_case]),
                   auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                   tokens: UserVerifyRequest = Depends(oauth2_scheme),
                   logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        link = await use_case.get_link(user, post_id)
        return JSONResponse(
            status_code=200,
            content=link.to_dict()
        )
    except (InvalidToken, ContentNotFound) as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.GET_LINK,
            message=str(error)
        )
        raise UnknownErrorException


@router.put('/{post_id}', summary='Update link')
@inject
async def update_link(post_id: int,
                      request_data: UpdateLinkRequest,
                      use_case: LinkUseCase = Depends(Provide[Container.link_use_case]),
                      auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                      tokens: UserVerifyRequest = Depends(oauth2_scheme),
                      logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        await use_case.update_link(user, post_id, request_data)
        return JSONResponse(
            status_code=200,
            content={'message': 'OK'}
        )
    except (InvalidToken, ContentNotFound) as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.UPDATE_LINK,
            message=str(error)
        )
        raise UnknownErrorException
