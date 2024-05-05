from typing import Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from src.schema.user import UserVerifyRequest


class OAuth2PasswordBearerWithCookie(OAuth2):

    def __init__(self,
                 tokenUrl: str,
                 scheme_name: Optional[str] = None,
                 scopes: Optional[Dict[str, str]] = None):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={'tokenUrl': tokenUrl, 'scopes': scopes})
        super().__init__(flows=flows, scheme_name=scheme_name)

    async def __call__(self, request: Request) -> UserVerifyRequest:
        # get jwt tokens from cookies and validate authorization schema
        access_token: str = request.cookies.get('access_token')
        refresh_token: str = request.cookies.get('refresh_token')
        scheme_access, access_token = get_authorization_scheme_param(access_token)
        scheme_refresh, refresh_token = get_authorization_scheme_param(refresh_token)
        if not access_token or scheme_access.lower() != 'bearer':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authenticated',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return UserVerifyRequest(
            access_token=access_token,
            refresh_token=refresh_token
        )


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl='/api/v1/log_in'
)
