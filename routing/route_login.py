from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.hashing import Hasher
from core.security import authenticate_user, create_access_token
from db.session import get_db

login_router = APIRouter()


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
