from src.user.models import User
from src.constants import USERS_KEY
from src.utils import randomInt
from src.jwt.encode_decode import encodeJWT
from src.response_models import Response
from src.user.response_models import LoginResponse
from src.user.request_models import SignupLoginUser as UserReq, TokenPayload
from typing import List
from datetime import date, timedelta
import src.db as db
import time
import bcrypt

def signup(req: UserReq) -> Response:
    users: List[dict] = db.get(USERS_KEY) or []
    response: Response = None
    
    if users:
        response = Response(data = None, code = 403, message="This is a one-user system and a user already exists.")
    else:
        user = User(id=randomInt(), email=req.email, password=bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()))

        users.append(dict(user))
        db.set(USERS_KEY, users)
        
        token = TokenPayload(user = user.email, expires = time.mktime((date.today() + timedelta(days=7)).timetuple()), randomizer = randomInt())
        data = LoginResponse(email = user.email, token = encodeJWT(dict(token)))

        response = Response(data = dict(data), code = 201, message="User signed up successfully")
    
    return response

def login(req: UserReq) -> Response:
    users: List[dict] = db.get(USERS_KEY)
    response: Response = None
    
    if users:
        user: dict = None

        for _user in users:
            if req.email == _user["email"] and bcrypt.checkpw(req.password.encode(), _user["password"].encode()):
                user = _user
        else:
            if user:
                token = TokenPayload(user = user["email"], expires = time.mktime((date.today() + timedelta(days=7)).timetuple()), randomizer = randomInt())
                data = LoginResponse(email = user["email"], token = encodeJWT(dict(token)))

                response = Response(data = dict(data), code = 200, message="User logged in succesfully")
            else:
                response = Response(data = None, code = 404, message="User not found")  
    else:
        response = Response(data = None, code = 404, message="User not found")
    
    return response

def doesUserExist() -> Response:
    users: List[dict] = db.get(USERS_KEY)
    response: Response = None
    
    if users and len(users):
        response = Response(data = True, code = 200, message="System user exists")
    else:
        response = Response(data = False, code = 200, message="System user does not exist")
    
    return response