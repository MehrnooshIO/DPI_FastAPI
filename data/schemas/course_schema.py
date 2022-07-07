from typing import Optional
from pydantic import BaseModel


class CourseSchema(BaseModel):
    courseName: str
    courseDetails: list[dict]
    



class CourseSchemaUpdate(BaseModel):
        courseInfo: list[dict]
