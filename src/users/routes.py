import sys
import os
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)
from fastapi import APIRouter, status, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from fastapi.responses import JSONResponse
from users.schemas import CreateUserRequest
from sqlalchemy.orm import Session
from core.security import oauth2_scheme
from users.services import create_user_account, authenticate_user
from .responses import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: CreateUserRequest, db: Session = Depends(get_db)):
    await create_user_account(data=data, db=db)
    payload = {"message": "User account has been created successfully created"}
    return JSONResponse(content=payload)

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
def login(form_data : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return JSONResponse(content={"Message": f"Welcome {user.first_name} {user.last_name}!", "Status": status.HTTP_200_OK})

@user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_detail(request: Request):
    return request.user
