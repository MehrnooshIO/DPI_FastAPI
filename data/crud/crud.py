from ..models.models import Base, User

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import db_config

# TODO: Move this to start up file
engine = create_engine(db_config['URI'])
Base.metadata.create_all(engine)

def db_create_user(email, password):
    with Session(bind=engine) as session:
        user = User(email=email, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user.id


def db_get_user_by_id(user_id):
    with Session(bind=engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
    return user


def db_get_user_by_email(user_email):
    with Session(bind=engine) as session:
        user = session.query(User).filter(User.email == user_email).first()
    return user