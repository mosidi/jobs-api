from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.operations.users import create_new_user, list_users
from db.session import get_db
from schemas.users import ShowUser, UserCreate

users_router = APIRouter()


@users_router.get(
    "/",
    summary="Get all users",
    response_model=List[ShowUser],
    description="Retrieves a list of all users registered in the system.\
    This endpoint may require authentication and authorization depending on your application's security requirements.",
)
def read_users(db: Session = Depends(get_db)):
    """
    Internal API Documentation:
    - **Endpoint**: GET /
    - **Purpose**: Fetch all registered users from the database.
    - **Auth Required**: Depends on application's security settings.
    - **Output**: A list of `ShowUser` model instances representing the users.

    This function queries the database for all user records and returns them.\
    Ensure proper handling of user data in compliance with privacy regulations.
    """
    users = list_users(db=db)
    return users


@users_router.post(
    "/register/",
    summary="Create new user",
    response_model=ShowUser,
    description="Registers a new user with the provided details. This is the entry point for new users to create an account in the system.",
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Internal API Documentation:
    - **Endpoint**: POST /register/
    - **Purpose**: Create a new user record in the database.
    - **Auth Required**: No, as this is for new user registration.
    - **Input**: `UserCreate` model with user details.
    - **Output**: `ShowUser` model instance of the newly created user.

    Ensures that the provided user details are valid and checks for any potential conflicts,\
    such as duplicate usernames or emails, before creating the user record in the database\
    . Implement appropriate error handling for such cases.
    """
    user = create_new_user(user=user, db=db)
    return user
