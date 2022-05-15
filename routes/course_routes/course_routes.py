from fastapi import APIRouter, Depends, Response, status
from data.crud import crud
from data.schemas.course_schema import CourseSchema

from helper.encrypt import get_user_id_from_token, oauth2_scheme


# Create a router for handling course information
def course_router() -> APIRouter:
    course_router = APIRouter()

    # Returns all courses for a user
    @course_router.get("/courses")
    def get_courses_of_user(token: str = Depends(oauth2_scheme)):
        id = get_user_id_from_token(token)
        courses = crud.db_get_user_courses(id)
        if not courses:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return courses
        

    # Returns a course details by id
    @course_router.get("/courses/{course_id}")
    def get_course(course_id: int, response: Response):
        course = crud.db_get_course_by_id(course_id)
        if not course:
            response.status = status.HTTP_404_NOT_FOUND
            return {"message": "Course not found"}
        return course

    # Edits a course by id
    @course_router.put("/courses/{course_id}")
    def edit_course(
            course_id: int,
            course_input: CourseSchema,
            response: Response,
            token: str = Depends(oauth2_scheme)):
        user_id = get_user_id_from_token(token)
        course = crud.db_get_course_by_id(course_id)
        if not course:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Course not found"}
        if course.user_id == user_id:
            crud.db_update_course(course_id, course_input)
            response.status_code = status.HTTP_201_CREATED
            return {"message": "Course updated"}
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message": "You are not allowed to edit this course"}


    # Create a new course for a user
    @course_router.post("/courses")
    def create_course(course_input: CourseSchema, response:Response , token: str = Depends(oauth2_scheme)):
        try:
            id = get_user_id_from_token(token)
            course_id = crud.db_create_user_course(
                id,
                course_input.name,
                course_input.fields,
            )
            response.status_code = status.HTTP_201_CREATED
            return {"course_id": course_id}
        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": str(e)}

    return course_router