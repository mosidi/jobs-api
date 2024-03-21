from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from .config import settings

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates an access token based on the provided data and expiration time.
    Args:
        data (dict): A dictionary containing the data to be encoded in the token.
        expires_delta (timedelta | None, optional): The expiration time for the token. Defaults to None.

    Returns:
        str: The encoded access token.

    Raises:
        None

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a refresh token based on the provided data and expiration time.

    Args:
        data (dict): A dictionary containing the data to be encoded in the token.
        expires_delta (Optional[timedelta], optional): The expiration time for the token. Defaults to None.

    Returns:
        str: The encoded refresh token.

    Raises:
        None

    """
    to_encode = data.copy()
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
