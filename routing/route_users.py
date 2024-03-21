from typing import List

from db.operations.users import create_new_user, list_users
from db.session import get_db
from fastapi import APIRouter, Depends
from schemas.users import ShowUser, UserCreate
from sqlalchemy.orm import Session

users_router = APIRouter()


@users_router.get("/", summary="Get all users", response_model=List[ShowUser])
def read_users(db: Session = Depends(get_db)):
    users = list_users(db=db)
    return users


@users_router.post("/register/", summary="Create new user", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
