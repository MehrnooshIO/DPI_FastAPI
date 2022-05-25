from data.models.models import User, UserCourse
from data.database import Base, engine

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from typing import Optional


# TODO: Move this to start up file
Base.metadata.create_all(engine)


# Retrieve a user from database by id
def db_get_user_by_id(user_id: int, db: Session) -> Optional[User]:
    """This function retrieves a user from the database by id.

    Args:
        user_id (int): The id of the user.
        db (Session): A database session.

    Returns:
        User | None: The user if found, None otherwise.
    """
    user: User | None = db.query(User).filter(User.id == user_id).first()
    return user


# Retrieve a user from database by email
def db_get_user_by_email(user_email: str, db: Session) -> Optional[User]:
    """This function retrieves a user from the database by email.

    Args:
        user_email (str): The email of the user.
        db (Session): A database session.

    Returns:
        User | None: The user if found, None otherwise.
    """
    user: User | None = db.query(User).filter(User.email == user_email).first()
    return user


# Retrieve list of all users in database
def db_get_users(db: Session) -> list[User]:
    """This function retrieves a list of all users in the database.

    Args:
        db (Session): A database session.

    Returns:
        list[User]: The list of all users.
    """
    users = db.query(User).all()
    return users


# Create a new user in database
def db_create_user(email: str, password: str, db: Session) -> int:
    """This function creates a new user in the database.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.
        db (Session): A database session.

    Returns:
        int: The id of the new user.
    """
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return int(user.id)