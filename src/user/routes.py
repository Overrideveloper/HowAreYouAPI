from fastapi import APIRouter, Body, Path, Depends
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.user.request_models import SignupLoginUser as User, ChangePassword
from src.user.response_models import LoginResponse
from src.utils import generate400ResContent, generate403ResContent, generate404ResContent
from typing import Union
import src.user.provider as provider
from src.jwt.jwt_bearer import JWTBearer

user = APIRouter()
jwt_bearer = JWTBearer()

@user.get('/status', summary="Get System User Status", description="Check if a system user exists or not. This is a one-user system.", response_model=Response[bool])
def getSystemUserStatus():
    data: Response[bool] = provider.doesUserExist()

    return JSONResponse(content = data.dict(), status_code = data.code)

@user.post('/signup', summary="Signup", description="Create a user account and get an authorization token", response_model=Response[LoginResponse],
responses={ 400: generate400ResContent(), 403: generate403ResContent("This is a one-user system and a user already exists."), 422: {} })
def signup(payload: User = Body(..., description="The user to sign up")):
    data: Union[Response[LoginResponse], Response] = provider.signup(payload)

    return JSONResponse(content = data.dict(), status_code = data.code)

@user.post('/login', summary="Login", description="Log in [as user] and get an authorization token", response_model=Response[LoginResponse],
responses={ 400: generate400ResContent(), 404: generate404ResContent("User"), 422: {}})
def login(payload: User = Body(..., description="The user to log in")):
    data: Union[Response[LoginResponse], Response] = provider.login(payload)

    return JSONResponse(content = data.dict(), status_code = data.code)

@user.put('/change-password/{id}', summary="Change Password", description="Change a user's password", response_model=Response[bool],
responses={ 400: generate400ResContent(), 404: generate404ResContent("User"), 422: {}}, dependencies=[Depends(jwt_bearer)])
def changePassword(id: int = Path(..., description="The ID of the user account whose password is to be changed"),
payload: ChangePassword = Body(..., description="The old and new passwords")):
    data: Union[Response[bool], Response] = provider.changePassword(id, payload)
    
    return JSONResponse(content = data.dict(), status_code = data.code)