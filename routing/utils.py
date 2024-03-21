from typing import Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    A custom OAuth2PasswordBearer class that uses cookies for authentication.
    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        """
        Initializes an instance of the class with the provided parameters.

        Args:
            tokenUrl (str): The URL for the token.
            scheme_name (Optional[str], optional): The name of the scheme. Defaults to None.
            scopes (Optional[Dict[str, str]], optional): The scopes for the token. Defaults to None.
            auto_error (bool, optional): Whether to automatically raise an error. Defaults to True.
        """
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Asynchronously handles the incoming request by extracting the access token from the request cookies.
        If the access token is not present or does not have the "Bearer" scheme, it raises an HTTPException
        with a status code of 401 UNAUTHORIZED and a detail message of "Not authenticated". If auto_error is
        False, it returns None instead.

        Parameters:
            request (Request): The incoming request object.

        Returns:
            Optional[str]: The extracted access token if it is present and has the "Bearer" scheme, else None.
        """
        authorization: str = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return
