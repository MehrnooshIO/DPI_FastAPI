from fastapi import APIRouter, Depends
from data.crud.crud import db_create_user_cource
from data.schemas.cource_schema import CourseSchema

from helper.encrypt import get_user_id_from_token



def cource_router() -> APIRouter:
    cource_router = APIRouter()

    @cource_router.get("/cources")
    def get_cources():
        pass

    @cource_router.get("/cources/{cource_id}")
    def get_cource(cource_id: int):
        pass

    @cource_router.post("/cources")
    def create_cource(cource_input: CourseSchema, id: int = Depends(get_user_id_from_token)):
        cource_id = db_create_user_cource(
            id,
            cource_input.name,
            cource_input.fields,
        )

    return cource_router