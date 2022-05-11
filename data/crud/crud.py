from ..models.models import Base, User, UserCources

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

def db_get_users():
    with Session(bind=engine) as session:
        users = session.query(User).all()
    return users


def db_create_user_cource(user_id, cource_name, cource_filds):
    with Session(bind=engine) as session:
        user_cource = UserCources(
            user_id=user_id,
            cource_name=cource_name,
            cource_filds=cource_filds,
            cource_info=None,
        )
        session.add(user_cource)
        session.commit()
        session.refresh(user_cource)
    return user_cource.id
