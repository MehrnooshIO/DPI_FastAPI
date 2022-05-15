from fastapi import APIRouter, Depends, HTTPException
from helper.encrypt import encrypt_password, check_password, create_token, get_user_id_from_token, oauth2_scheme


from data.schemas.user_schema import UserSchema
from data.crud import crud





# Create a router for handling user authentication and information
def auth_router() -> APIRouter:
    user_router = APIRouter()

    # Handles user signup
    @user_router.post("/signup")
    def signup(user_input: UserSchema):
        hashed_pass = encrypt_password(user_input.password)
        user_id = crud.db_create_user(user_input.email, hashed_pass)
        return {"user_id": user_id}

    # Handles user login and return a token if user is valid
    @user_router.post("/token")
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

    # Returns the list of all users
    @user_router.get("/users")
    def get_users(token: str = Depends(oauth2_scheme)):
        users = crud.db_get_users()
        return users

    # Returns details of current user
    @user_router.get("/users/me")
    def read_users_me(token: str = Depends(oauth2_scheme)):
        id = get_user_id_from_token(token)
        user = crud.db_get_user_by_id(id)
        return user

    return user_router