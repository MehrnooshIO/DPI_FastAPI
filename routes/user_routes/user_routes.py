from email.policy import HTTP
from fastapi import APIRouter, HTTPException
from helper.encrypt import encrypt_password, check_password, create_token

from data.schemas.user_schema import UserSchema
from data.crud import crud

def auth_router() -> APIRouter:
    user_router = APIRouter()

    @user_router.post("/signup")
    def signup(user_input: UserSchema):
        hashed_pass = encrypt_password(user_input.password)
        user_id = crud.db_create_user(user_input.email, hashed_pass)
        return {"user_id": user_id}

    @user_router.post("/login")
    def login(user_input: UserSchema):
        user = crud.db_get_user_by_email(user_input.email)
        if not user:
            raise HTTPException(status_code=400, detail="Wrong Credential")
        hashed_pass = encrypt_password(user_input.password)
        if not check_password(user_input.password, user.password):
            raise HTTPException(status_code=400, detail="Wrong Credential")
        else:
            token = create_token(user.id)
            return {"jwt": token}
          

    return user_router