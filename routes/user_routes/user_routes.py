from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from helper.encrypt import (
    encrypt_password, 
    check_password, 
    create_token, 
    get_user_id_from_token, 
    oauth2_scheme
)

from data.schemas.user_schema import UserSchema
from data.crud import user_crud
from data.database import get_db

# Create a router for handling user authentication and information
def auth_router() -> APIRouter:
    user_router = APIRouter()

    # Handles user signup
    @user_router.post("/signup")
    def signup(user_input: UserSchema, response:Response, db: Session = Depends(get_db)):
        user = user_crud.db_get_user_by_email(user_input.email, db)
        if user:
            response.status_code = status.HTTP_409_CONFLICT
            return {
                "status": "error",
                "message": "User with this email already exists"
            }
        hashed_pass = encrypt_password(user_input.password)
        user_id = user_crud.db_create_user(user_input.email, hashed_pass, db)
        return {
            "statusCode": status.HTTP_201_CREATED,
            "title": "Success",
            "statusText": "User created successfully",
        }

    # Handles user login and return a token if user is valid
    @user_router.post("/token")
    def login(user_input: UserSchema, db: Session = Depends(get_db)):
        user = user_crud.db_get_user_by_email(user_input.email, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Credential")
        hashed_pass = encrypt_password(user_input.password)
        if not check_password(user_input.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "title": "Wrong Credential",
                    "statusText": "Bad Request",
                    "errorText": "Username or Password is incorrect"
                }
            )
        else:
            token = create_token(user.id)
            return {
                "statusCode": status.HTTP_200_OK,
                "title": "Success",
                "statusText": "OK",
                "token": token,
            }

    # Returns the list of all users
    @user_router.get("/users")
    def get_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        users = user_crud.db_get_users(db)
        return users

    # Returns details of current user
    @user_router.get("/users/me")
    def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        id = get_user_id_from_token(token)
        user = user_crud.db_get_user_by_id(id, db)
        return user

    return user_router