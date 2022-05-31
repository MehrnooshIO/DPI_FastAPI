from aifc import Error
from data.models.models import UserCourse
from data.database import engine
from helper.link import create_link

from sqlalchemy import JSON, create_engine
from sqlalchemy.orm import Session

from typing import Optional


def db_create_user_course(
    user_id,
    course_name,
    course_filds,
    db: Session
    ) -> Optional[Error]:
    """This function creates a new course for a user

    Args:
        user_id (_type_): The id of the user
        course_name (_type_): The name of the course which specified by the user
        course_filds (_type_): The fields of the course which specified by the user
        db (Session): The database session

    Returns:
        None | Error: If the course is created successfully, return None, otherwise return Error
    """
    try:
        user_course = UserCourse(
        user_id=user_id,
        course_name=course_name,
        course_filds=course_filds,
        course_info=None,
        course_link= create_link()
        )
        db.add(user_course)
        db.commit()
        db.refresh(user_course)
        return
    except Exception as e:
        return e


def db_get_user_courses(user_id, db: Session) -> list[UserCourse]:
    """This function return the list of all courses of a user based on user id

    Args:
        user_id (_type_): The id of the user
        db (Session): The database session

    Returns:
        list[UserCourse]: The list of all courses of a user
    """
    user_courses = db.query(UserCourse).filter(UserCourse.user_id == user_id).all()
    return user_courses


def db_get_course_by_id(course_id: int, db: Session) -> Optional[UserCourse]:
    """This function return the course details based on course id

    Args:
        course_id (int): The id of the course
        db (Session): The database session

    Returns:
        UserCourse | None: The course details if the course exists, otherwise return None
    """
    course: UserCourse| None = db.query(UserCourse).filter(UserCourse.id == course_id).first()
    return course


def db_update_course(course_id: int, course_info: dict, db: Session) -> Optional[Error]:
    """This function updates the course details based on course id

    Args:
        course_id (int): The id of the course
        course_info (dict): The course details which specified by the user in the form of a dictionary
        db (Session): The database session
    """
    try:
        course = db.query(UserCourse).filter(UserCourse.id == course_id).first()
        course.course_info = course_info
        db.add()
        db.commit()
        return
    except Exception as e:
        return e


def db_get_course_by_name(course_name: str, db: Session) -> Optional[UserCourse]:
    course = db.query(UserCourse).filter(UserCourse.course_name == course_name).first()
    return course 

def db_get_all_courses(db:Session):
    course=db.query(UserCourse).all()
    return course
    
