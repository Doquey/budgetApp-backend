"""
create user and register objectives.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.dependencies.authentication import authenticate_user, create_access_token, get_password_hashed
from app.db.Models import User, Token
from app.db.users import users_db

ACCESS_TOKEN_EXPIRE_MINUTES = 60


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", tags=["user"])
def register_new_user(user: User):
    try:
        user.password = get_password_hashed(user.password)
        users_db.put_item(user.model_dump(), "USERS")
        return "User Created Sucessfully"
    except Exception as e:
        raise e


@router.post("/login", tags=["user"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
