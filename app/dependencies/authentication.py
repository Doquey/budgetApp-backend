""" 
how authentication with fastapi works:

    First we create an end-point to create an user, as we already did.
    Then we create an end-point to log the user in. In this endpoint what it will do is:
        - It will verify that the name and password passed are in our database.
        - If it is, it will then create and return a token to the front-end.
        - The front-end will store that token, and will pass it with a Autorization header, with a bearer + token value.
        - Then, all of our end-points that need authentication, will run a Dependency that checks if there is a token togather with the
        Autorization header.
        - To do this last part, it seems we pass in this to the end-point:
            
            oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


            @app.get("/items/")
            async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
                return {"token": token}

        Notice that our oauth2_scheme will look for the token at the url ./token. Therefore I can pass which url I
        want it to look for the token at.

        - Actually we are not passing the oauth2_scheme dependency directly to the protected end-point. We are 
        creating a get_current_user function and passing the oauth2_scheme to it as a dependency, and then we pass
        the get_current_user function as a dependency to the protected end-points. This way we can get and see if the token exists
        using the oauth2_scheme, then we can use that token to get the current activate user.

"""
import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from app.db.Models import User, TokenData
from app.db.users import users_db
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hashed(password: str):
    return pwd_context.hash(password)


def get_user(username: str):
    user = users_db.get_item(username, "USERS")
    if user is not None:
        return User(**user)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
