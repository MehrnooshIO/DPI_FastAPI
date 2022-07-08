from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from data.crud.course_crud import db_get_all_courses, db_get_course_link
from data.crud import course_crud
from data.schemas.course_schema import CourseSchema, CourseSchemaUpdate
from data.database import get_db

from helper.encrypt import get_user_id_from_token, oauth2_scheme

# Create a router for handling course information
def course_router() -> APIRouter:
    course_router = APIRouter()

    # Returns all courses for a user
    @course_router.get("/user_courses")
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
                    "errorText": "دوره ای یافت نشد"
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
    def get_course(course_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
        user_id = get_user_id_from_token(token)
        course = course_crud.db_get_course_by_id(course_id, db)

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "title": "Not Found",
                    "statusText": "Not Found",
                    "errorText": "دوره ای با این مشخصات وجود ندارد"
                }
            )


        if course.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "statusCode": status.HTTP_403_FORBIDDEN,
                    "title": "Forbidden",
                    "statusText": "Forbidden",
                    "errorText": "شمااجازه مشاهده این دوره راندارید"
                }
            )
        
        return {
            "statusCode": status.HTTP_200_OK,
            "title": "Success",
            "statusText": "OK",
            "courseDetails": course_crud.db_get_course_details(course.id, db),
            "course": course
        }

    # Edits a course by id
    @course_router.put("/courses/{course_id}")
    def edit_course(
        course_id: int,
        course_input: CourseSchemaUpdate,
        response: Response,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
    ):
        user_id = get_user_id_from_token(token)
        course = course_crud.db_get_course_by_id(course_id, db)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "statusCode": status.HTTP_404_NOT_FOUND,
                    "title": "Not Found",
                    "statusText": "Not Found",
                    "errorText": "دوره ای پیدا نشد"
                }
            )
        
        if course.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "statusCode": status.HTTP_403_FORBIDDEN,
                    "title": "Forbidden",
                    "statusText": "Forbidden",
                    "errorText": "شما اجازه تغییر این دوره را ندارید"
                }
            )
        else:
            course_crud.db_course_insert(course, course_input, db)

    # FIXME: Handling wrong token
    # Create a new course for a user
    @course_router.post("/courses")
    def create_course(
                    course_input: CourseSchema,
                    response: Response,
                    token: str = Depends(oauth2_scheme),
                    db: Session = Depends(get_db),
        ):
        # Cheks if this course already exists
        id = get_user_id_from_token(token)
        table_name = str(id) + "_" + course_input.courseName
        course = course_crud.db_get_course_by_name(table_name, db)
        if course:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "statusCode": status.HTTP_409_CONFLICT,
                    "title": "Conflict",
                    "statusText": "دوره دیگری با این نام وجود دارد",
                }
            )
        try:
            course_id = course_crud.db_create_course(
                id,
                course_input,
                db
            )
            response.status_code = status.HTTP_201_CREATED
            return {
                "statusCode": status.HTTP_201_CREATED,
                "title": "Created",
                "statusText": "دوره جدید ایجاد شد",
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


    @course_router.get("/courses")
    def get_all_courses( db: Session = Depends(get_db)):
        courses=db_get_all_courses(db)
        return {
            "statuseCode":status.HTTP_200_OK,
            "title":"successful",
            "courseList":courses
        }
    
    @course_router.get("/{course_link}")
    def get_course_by_link(course_link:str,db:Session=Depends(get_db)):
        course = db_get_course_link(course_link, db)
        return {
            "statuseCode":status.HTTP_200_OK,
            "title":"successful",
            "courseDetail":course
        }

    # @course_router.delete("/courses/{course_id}")
    # def delete_course(course_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    #     user_id = get_user_id_from_token(token)
    #     course = course_crud.db_get_course_by_id(course_id, db)
    #     if not course:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail={
    #                 "statusCode": status.HTTP_404_NOT_FOUND,
    #                 "title": "Not Found",
    #                 "statusText": "Not Found",
    #                 "errorText": "دوره ای پیدا نشد"
    #             }
    #         )
        
    #     if course.user_id != user_id:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail={
    #                 "statusCode": status.HTTP_403_FORBIDDEN,
    #                 "title": "Forbidden",
    #                 "statusText": "Forbidden",
    #                 "errorText": "شما اجازه تغییر این دوره را ندارید"
    #             }
    #         )

    return course_router