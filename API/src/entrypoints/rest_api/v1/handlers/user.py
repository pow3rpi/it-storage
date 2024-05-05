from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.core.config import cookie_options, SIGN_UP_REDIRECT_URL
from src.core.enums import APIHandlerEnum
from src.core.exceptions.user import (
    UsernameExists, WrongPassword, EqualPasswords, InvalidToken,
    InvalidCredentials, NonActivatedAccount, EmailExists
)
from src.entrypoints.container import Container
from src.entrypoints.core import oauth2_scheme
from src.interface.logger import LoggerInterface
from src.interface.services.auth import AuthServiceInterface
from src.schema.user import (
    UserSignUpRequest, UserLogInRequest, UserVerifyRequest,
    UserUpdateRequest, ChangePasswordRequest, UserLogInResponse
)
from src.usecase.auth.log_in import LogInUseCase
from src.usecase.auth.password import ChangePasswordUseCase
from src.usecase.auth.sign_up import SignUpUseCase
from src.usecase.auth.update import UpdateUserUseCase
from ..config import UnknownErrorException

auth_router = APIRouter(tags=['Auth'])


@auth_router.post('/sign_up', summary='Create new user')
@inject
async def sign_up(request_data: UserSignUpRequest,
                  use_case: SignUpUseCase = Depends(Provide[Container.sign_up_use_case]),
                  logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        await use_case.sign_up(request_data)
        return JSONResponse(
            status_code=201,
            content={'message': 'OK'}
        )
    except (UsernameExists, EmailExists) as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.SIGN_UP,
            message=str(error)
        )
        raise UnknownErrorException


@auth_router.get('/activate_account', summary='Activate account')
@inject
async def verify_sign_up(token: str,
                         username: str,
                         use_case: SignUpUseCase = Depends(Provide[Container.sign_up_use_case]),
                         logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        is_verified = await use_case.verify_sign_up(token, username)
        if is_verified:
            return RedirectResponse(SIGN_UP_REDIRECT_URL, status_code=303)
        return Response(status_code=406)
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.ACTIVATE_ACCOUNT,
            message=str(error)
        )
        raise UnknownErrorException


@auth_router.post('/log_in', summary='Create access and refresh tokens for user', response_model=UserLogInResponse)
@inject
async def log_in(response: Response,
                 form_data: OAuth2PasswordRequestForm = Depends(),
                 use_case: LogInUseCase = Depends(Provide[Container.log_in_use_case]),
                 logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        data = UserLogInRequest(
            username=form_data.username,
            password=form_data.password
        )
        tokens = await use_case.log_in(data)
        for key, value in tokens:
            response.set_cookie(key, f'Bearer {value}', **cookie_options)
        return tokens
    except (InvalidCredentials, NonActivatedAccount) as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.LOG_IN,
            message=str(error)
        )
        raise UnknownErrorException


"""
- If you want to send tokens in request header, you need to:
1) define security variable = HTTPBearer()
2) use "credentials: HTTPAuthorizationCredentials = Security(security)" as a parameter
    - to get access to the token use ".credentials" method
"""


@auth_router.post('/verify_user', summary='Verify user by validating tokens', status_code=202)
@inject
async def verify_user(response: Response,
                      tokens: UserVerifyRequest = Depends(oauth2_scheme),
                      auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                      logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        new_tokens = await auth_service.verify_user(tokens)
        if new_tokens:
            for key, value in new_tokens:
                response.set_cookie(key, f'Bearer {value}', **cookie_options)
        return new_tokens
    except InvalidToken as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.VERIFY_USER,
            message=str(error)
        )
        raise UnknownErrorException


@auth_router.post('/log_out', summary='Delete tokens')
async def log_out(response: Response,
                  logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        response.delete_cookie('access_token',
                               **{key: value for key, value in cookie_options.items() if key != 'expires'})
        response.delete_cookie('refresh_token',
                               **{key: value for key, value in cookie_options.items() if key != 'expires'})
        response.status_code = 200
        return response
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.LOG_OUT,
            message=str(error)
        )
        raise UnknownErrorException


@auth_router.get('/get_me', summary='Get profile info')
@inject
async def get_me(auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                 tokens: UserVerifyRequest = Depends(oauth2_scheme),
                 logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        return JSONResponse(
            status_code=200,
            content={key: value for key, value in user.__dict__.items() if
                     key in ('username', 'email', 'first_name', 'last_name')}
        )
    except InvalidToken as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.GET_ME,
            message=str(error)
        )
        raise UnknownErrorException


@auth_router.put('/update_profile', summary='Update profile info')
@inject
async def update_profile(request_data: UserUpdateRequest,
                         use_case: UpdateUserUseCase = Depends(Provide[Container.update_user_use_case]),
                         auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                         tokens: UserVerifyRequest = Depends(oauth2_scheme),
                         logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        await use_case.update_user(user, request_data)
        response = JSONResponse(
            status_code=200,
            content={'message': 'OK'}
        )
        # refresh tokens is username has been changed
        if user.username != request_data.username:
            response.set_cookie('access_token',
                                f'Bearer {auth_service.create_access_token(request_data.username)}',
                                **cookie_options)
            response.set_cookie('refresh_token',
                                f'Bearer {auth_service.create_refresh_token(request_data.username)}',
                                **cookie_options)
        return response
    except (UsernameExists, EmailExists, InvalidToken) as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.UPDATE_PROFILE,
            message=str(error)
        )
        raise UnknownErrorException


@auth_router.put('/change_password', summary='Change user password')
@inject
async def change_password(request_data: ChangePasswordRequest,
                          use_case: ChangePasswordUseCase = Depends(Provide[Container.change_password_use_case]),
                          auth_service: AuthServiceInterface = Depends(Provide[Container.auth_service]),
                          tokens: UserVerifyRequest = Depends(oauth2_scheme),
                          logger: LoggerInterface = Depends(Provide[Container.logger])):
    try:
        user = await auth_service.get_current_user(tokens.access_token)
        await use_case.change_password(user, request_data)
        return JSONResponse(
            status_code=200,
            content={'message': 'OK'}
        )
    except (InvalidToken, EqualPasswords, WrongPassword) as error:
        raise HTTPException(
            status_code=422,
            detail=int(str(error))
        )
    except Exception as error:
        logger.log_error(
            handler=APIHandlerEnum.CHANGE_PASSWORD,
            message=str(error)
        )
        raise UnknownErrorException
