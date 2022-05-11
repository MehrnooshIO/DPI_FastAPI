from ..models.models import Base, User, UserCourse

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import db_config

# TODO: Move this to start up file
engine = create_engine(db_config['URI'])
Base.metadata.create_all(engine)


# Create a new user in database
def db_create_user(email, password):
    with Session(bind=engine) as session:
        user = User(email=email, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user.id


# Retrieve a user from database by id
def db_get_user_by_id(user_id):
    with Session(bind=engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
    return user


# Retrieve a user from database by email
def db_get_user_by_email(user_email):
    with Session(bind=engine) as session:
        user = session.query(User).filter(User.email == user_email).first()
    return user


# Retrieve list of all users in database
def db_get_users():
    with Session(bind=engine) as session:
        users = session.query(User).all()
    return users


def db_create_user_course(user_id, course_name, course_filds):
    with Session(bind=engine) as session:
        user_course = UserCourse(
            user_id=user_id,
            course_name=course_name,
            course_filds=course_filds,
            course_info=None,
        )
        session.add(user_course)
        session.commit()
        session.refresh(user_course)
    return user_course.id


def db_get_user_courses(user_id):
    with Session(bind=engine) as session:
        user_courses = session.query(UserCourse).filter(UserCourse.user_id == user_id).all()
    return user_courses


def db_get_course_by_id(course_id):
    with Session(bind=engine) as session:
        course = session.query(UserCourse).filter(UserCourse.id == course_id).first()
    return course


def db_update_course(course_id, course_info):
    with Session(bind=engine) as session:
        course = session.query(UserCourse).filter(UserCourse.id == course_id).first()
        course.course_info = course_info
