from sqlalchemy.orm import Session

from db.models.users import User
from core.hashing import Hasher
from schemas.users import UserCreate


def create_new_user(user: UserCreate, db: Session):
    """
    Creates a new user in the database with the provided user information.

    Args:
        user (UserCreate): The user information to create a new user.
        db (Session): The database session to use for creating the user.

    Returns:
        User: The newly created user object.
    """
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def list_users(db: Session):
    """
    Retrieves a list of all users from the database.

    Parameters:
        db (Session): The database session object.

    Returns:
        List[User]: A list of User objects representing all the users in the database.
    """
    users = db.query(User).all()
    return users


def get_user_by_email(email: str, db: Session):
    """
    A function that retrieves a user from the database based on their email address.

    Parameters:
    email (str): The email address of the user to retrieve.
    db (Session): The database session to query.

    Returns:
    User: The user object corresponding to the provided email, or None if not found.
    """
    user = db.query(User).filter(User.email == email).first()
    return user
