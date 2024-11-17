from pydantic import BaseModel, Field
from enum import Enum


class User(BaseModel):
    name: str = Field(description="User name", examples=["Luis"])
    username: str = Field(
        description="Name that the user uses to login", examples=["luis123"])
    password: str = Field(description="Users password")
    email: str = Field(description="User's email",
                       examples=["luis123@blabla.com"])
    phone: str = Field(description="Users phone", examples=["31988888888"])


class PurchaseType(Enum):
    FIXO = 0,
    METAS = 1,
    CONHECIMENTO = 2,
    PRAZER = 3,
    INVESTIMENTO = 4


class Purchase(BaseModel):
    major_category: str = Field(
        "The category that this purchase belongs to", examples=["FIXO"])
    value: float = Field("The value of the purchase", examples=["155.20"])
    description: str = Field("A brief description of this purchase", examples=[
                             "Bought a drink in a bar"])
    general_category: str = Field(
        "A real worl category of the purchase", examples=["Coisas pro carro", "Coisas pra casa", "Jantar fora"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBudgetSettings(BaseModel):
    pass
