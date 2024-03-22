from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import settings
from core.hashing import Hasher
from db.models.users import User
from db.operations.login import get_user
from db.session import get_db
from routing.utils import OAuth2PasswordBearerWithCookie

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 60 * 24 * 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 60 * 24 * 30


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/token")


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def authenticate_user(username: str, password: str, db: Session):
    """
    Authenticates a user with the given username and password using the provided database session.

    Args:
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.
        db (Session): The database session to use for authentication.

    Returns:
        Union[bool, User]: Returns the authenticated user if successful, otherwise False.
    """
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


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


def get_current_user_from_token(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
) -> User:
    """
    Get the current user from the provided token.

    Parameters:
    - token: str = Depends(reuseable_oauth)
    - db: Session = Depends(get_db)

    Returns:
    - The user retrieved from the token or the invalid_credentials_exception.
    """
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise invalid_credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise invalid_credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise invalid_credentials_exception
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Retrieves the current active user from the token.

    Parameters:
        current_user (User, optional): The current user obtained from the token. Defaults to the result of the `get_current_user_from_token` dependency.

    Raises:
        HTTPException: If the current user is disabled.

    Returns:
        User
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
