from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.user.request_models import SignupLoginUser as User
import src.user.provider as provider

user = APIRouter()

@user.get('/status')
def getSystemUserStatus():
    data: Response = provider.doesUserExist()

    return JSONResponse(content = dict(data), status_code = data.code)

@user.post('/signup')
def signup(payload: User):
    data: Response = provider.signup(payload)

    return JSONResponse(content = dict(data), status_code = data.code)

@user.post('/login')
def login(payload: User):
    data: Response = provider.login(payload)

    return JSONResponse(content = dict(data), status_code=data.code)
        