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
from src.schema.tutorial import CreateTutorialRequest, UpdateTutorialRequest
from src.schema.user import UserVerifyRequest
from src.usecase.blog.tutorial import TutorialUseCase
from ..config import UnknownErrorException

router = APIRouter(prefix='/tutorials', tags=['Tutorial'])


@router.post('/create', summary='Create tutorial')
@inject
async def create_tutorial(request_data: CreateTutorialRequest,
                          use_case: TutorialUseCase = Depends(Provide[Container.tutorial_use_case]),
                          auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                          tokens: UserVerifyRequest = Depends(oauth2_scheme),
                          logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        await use_case.create_tutorial(user, request_data)
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
            handler=APIHandlerEnum.CREATE_TUTORIAL,
            message=str(error)
        )
        raise UnknownErrorException


@router.get('/{post_id}', summary='Get tutorial')
@inject
async def get_tutorial(post_id: int,
                       use_case: TutorialUseCase = Depends(Provide[Container.tutorial_use_case]),
                       auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                       tokens: UserVerifyRequest = Depends(oauth2_scheme),
                       logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        tutorial = await use_case.get_tutorial(user, post_id)
        return JSONResponse(
            status_code=200,
            content=tutorial.to_dict()
        )
    except (InvalidToken, ContentNotFound) as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.GET_TUTORIAL,
            message=str(error)
        )
        raise UnknownErrorException


@router.put('/{post_id}', summary='Update tutorial')
@inject
async def update_tutorial(post_id: int,
                          request_data: UpdateTutorialRequest,
                          use_case: TutorialUseCase = Depends(Provide[Container.tutorial_use_case]),
                          auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                          tokens: UserVerifyRequest = Depends(oauth2_scheme),
                          logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        await use_case.update_tutorial(user, post_id, request_data)
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
            handler=APIHandlerEnum.UPDATE_TUTORIAL,
            message=str(error)
        )
        raise UnknownErrorException
