import belvo.client
from fastapi import APIRouter, Depends
from app.dependencies.authentication import get_current_active_user
from typing import Annotated
from app.db.Models import User
from dotenv import load_dotenv
import belvo
import os

load_dotenv()

SECRET_ID = os.getenv("SECRET_ID")
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")

belvo_client = belvo.Client(
    SECRET_ID, SECRET_PASSWORD, "https://sandbox.belvo.com")

router = APIRouter(prefix="/data", tags=["data"])


@router.get('/monthly_data')
def get_monthly_data_for_user(user: Annotated[User, Depends(get_current_active_user)]):
    pass
