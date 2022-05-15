from typing import Optional
from pydantic import BaseModel


class CourseSchema(BaseModel):
    name: str
    fields: dict
    info: Optional[dict] = None