from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from data.crud import course_crud
from data.schemas.course_schema import CourseSchema
from data.database import get_db

from helper.encrypt import get_user_id_from_token, oauth2_scheme


# Create a router for handling course information
def course_router() -> APIRouter:
    course_router = APIRouter()

    # Returns all courses for a user
    @course_router.get("/courses")
    def get_courses_of_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
        id = get_user_id_from_token(token)
        courses = course_crud.db_get_user_courses(id, db)
        if not courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "title": "Not Found",
                    "statusText": "Not Found",
                    "errorText": "No courses found for this user"
                }
            )
        return {
            "statusCode": status.HTTP_200_OK,
            "title": "Success",
            "statusText": "OK",
            "courses": courses
        }
        

    # Returns a course details by id
    @course_router.get("/courses/{course_id}")
    def get_course(course_id: int, db: Session = Depends(get_db)):
        course = course_crud.db_get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "title": "Not Found",
                    "statusText": "Not Found",
                    "errorText": "No course found with this id"
                }
            )
        return {
            "statusCode": status.HTTP_200_OK,
            "title": "Success",
            "statusText": "OK",
            "course": course
        }

    # Edits a course by id
    @course_router.put("/courses/{course_id}")
    def edit_course(
        course_id: int,
        course_input: CourseSchema,
        response: Response,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
    ):
        user_id = get_user_id_from_token(token)
        course = course_crud.db_get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "title": "Not Found",
                    "statusText": "Not Found",
                    "errorText": "No course found with this id"
                }
            )
        
        if course.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "statusCode": status.HTTP_403_FORBIDDEN,
                    "title": "Forbidden",
                    "statusText": "Forbidden",
                    "errorText": "You are not allowed to edit this course"
                }
            )
        else:
            result = course_crud.db_update_course(course_id, course_input, db)
            if isinstance(result, Exception):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "statusCode": status.HTTP_400_BAD_REQUEST,
                        "title": "Bad Request",
                        "statusText": "Bad Request",
                        "errorText": "Error updating course"
                    }
                )
            response.status_code = status.HTTP_201_CREATED
            return {
                "statusCode": status.HTTP_201_CREATED,
                "title": "Success",
                "statusText": "OK",
            }


    # Create a new course for a user
    @course_router.post("/courses")
    def create_course(
        course_input: CourseSchema,
        response: Response,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
    ):
        try:
            id = get_user_id_from_token(token)
            course_id = course_crud.db_create_user_course(
                id,
                course_input.name,
                course_input.fields,
                db
            )
            response.status_code = status.HTTP_201_CREATED
            return {
                "statusCode": status.HTTP_201_CREATED,
                "title": "Success",
                "statusText": "OK",
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "title": "Internal Server Error",
                    "statusText": "Internal Server Error",
                }
            )

    return course_router