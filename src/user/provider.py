from src.user.models import User
from src.constants import USERS_KEY
from src.utils import randomInt
from src.jwt.encode_decode import encodeJWT
from src.response_models import Response
from src.user.response_models import LoginResponse
from src.user.request_models import SignupLoginUser as UserReq, TokenPayload
from typing import List, Union
from datetime import date, timedelta
import src.db as db
import time
import bcrypt

def signup(req: UserReq) -> Union[Response[LoginResponse], Response]:
    users: List[dict] = db.get(USERS_KEY) or []
    response: Union[Response[LoginResponse], Response] = None
    
    if users:
        response = Response(data = None, code = 403, message="This is a one-user system and a user already exists.")
    else:
        user = User(id=randomInt(), email=req.email, password=bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()))

        users.append(user.dict())
        db.set(USERS_KEY, users)
        
        token = TokenPayload(user = user.email, expires = time.mktime((date.today() + timedelta(days=7)).timetuple()), randomizer = randomInt())
        loginRes = LoginResponse(email = user.email, token = encodeJWT(token.dict()))

        response = Response[LoginResponse](data = loginRes, code = 201, message="User signed up successfully")
    
    return response

def login(req: UserReq) -> Union[Response[LoginResponse], Response]:
    users: List[dict] = db.get(USERS_KEY)
    response: Union[Response[LoginResponse], Response] = None
    
    if users:
        user: dict = None

        for _user in users:
            if req.email == _user["email"] and bcrypt.checkpw(req.password.encode(), _user["password"].encode()):
                user = _user
        else:
            if user:
                token = TokenPayload(user = user["email"], expires = time.mktime((date.today() + timedelta(days=7)).timetuple()), randomizer = randomInt())
                loginRes = LoginResponse(email = user["email"], token = encodeJWT(token.dict()))

                response = Response[LoginResponse](data = loginRes, code = 200, message="User logged in succesfully")
            else:
                response = Response(data = None, code = 404, message="User not found")  
    else:
        response = Response(data = None, code = 404, message="User not found")
    
    return response

def doesUserExist() -> Response[bool]:
    users: List[dict] = db.get(USERS_KEY)
    response: Response[bool] = None
    
    if users and len(users):
        response = Response[bool](data = True, code = 200, message="System user exists")
    else:
        response = Response[bool](data = False, code = 200, message="System user does not exist")
    
    return response