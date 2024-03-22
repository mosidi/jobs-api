from sqlalchemy.orm import Session

from db.models.users import User


def get_user(username: str, db: Session):
    """
    Retrieves a user from the database based on the provided username.

    Parameters:
    username (str): The username of the user to retrieve.
    db (Session): The database session.

    Returns:
    User: The user object if found, otherwise None."""
    user = db.query(User).filter(User.email == username).first()
    return user
