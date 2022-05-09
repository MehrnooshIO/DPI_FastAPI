from fastapi import APIRouter

from data.schemas.user_schema import UserSignUpSchema

def auth_router() -> APIRouter:
    user_router = APIRouter()

    @user_router.get("/signup")
    def signup(user_input: UserSignUpSchema):

        return {"message": "Signup"}



    return user_router