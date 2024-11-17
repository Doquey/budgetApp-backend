from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from .routes import user
from .routes import control
from .db.createtables import create_tables

app = FastAPI()


origins = [
    "http://localhost:3000",  # Frontend running on localhost
    # Add other origins if needed (e.g., your production URL)
]

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)


app.include_router(control.router)
app.include_router(user.router)


@app.on_event("startup")
def on_startup():
    # Call the function to create tables
    create_tables()
