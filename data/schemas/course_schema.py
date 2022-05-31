from typing import Optional
from pydantic import BaseModel


class CourseSchema(BaseModel):
    name: str
    fields: list[dict]
    info: Optional[dict] = None