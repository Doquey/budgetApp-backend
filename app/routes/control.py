""""
get data to show the user how he is doing, compared to his objectives
"""


from fastapi import APIRouter, Depends
from typing import Annotated
from app.db.Models import Purchase, User
from app.dependencies.authentication import get_current_active_user

router = APIRouter(prefix="/control", tags=["control"])


@router.post("/register_purchase", tags=["control"])
def register_user_purchase(purchase: Purchase, user: Annotated[User, Depends(get_current_active_user)]):
    pass
