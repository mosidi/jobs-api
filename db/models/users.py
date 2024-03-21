from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """
    A User represents a user of the application, with details such as username, email, phone number,
    hashed password, and whether the user is active or a superuser. The class has a one-to-many relationship
    with the Job class, where a User can have many Jobs.

    Attributes:
        id (Integer): The unique id of the User.
        username (String): The username of the User.
        email (String): The email of the User.
        phone_number (String): The phone number of the User.
        hashed_password (String): The hashed password of the User.
        is_active (Boolean): Whether the User is active.
        is_superuser (Boolean): Whether the User is a superuser.
        jobs (Relationship): The relationship with the Job class, where a User can have many Jobs.
    """

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone_number = Column(String, nullable=True, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    jobs = relationship("Job", back_populates="job_owner")
