from datetime import timedelta

from routing.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.models.users import User
from db.operations.login import get_user
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
login_router = APIRouter()


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


@login_router.post("/token", summary="Login user")
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    A function to handle user login and generate an access token.

    Parameters:
    - response: FastAPI Response object
    - form_data: OAuth2PasswordRequestForm object containing username and password
    - db: SQLAlchemy Session object

    Returns:
    A dictionary containing the generated access token and its type.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expire
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
