from src.user.models import User
from src.constants import USERS_KEY
from src.utils import randomInt, encodeJWT
from src.response_models import Response
from src.user.response_models import LoginResponse
from src.user.request_models import SignupLoginUser as UserReq
from typing import List
from datetime import date, timedelta
import src.db as db
import time
import bcrypt

def signup(_req: UserReq) -> Response:
    req = dict(_req)
    users: List[User] = db.get(USERS_KEY) or []
    
    if users:
        return Response(data = None, code = 403, message="This is a one-user system and a user already exists.")
    else:
        user = dict(User(id=randomInt(), email=req["email"], password=bcrypt.hashpw(req["password"].encode(), bcrypt.gensalt())))
        users.append(user)
        db.set(USERS_KEY, users)
        
        token = { "user": req["email"], "expires": time.mktime((date.today() + timedelta(days=7)).timetuple()) }
        data = LoginResponse(email = user["email"], token = encodeJWT(token))

        return Response(data = dict(data), code = 201, message="User signed up successfully")

def login(_req: UserReq) -> Response:
    req = dict(_req)
    users: List[User] = db.get(USERS_KEY) or []
    
    if users:
        user: User = None

        for _user in users:
            if req["email"] == _user["email"] and bcrypt.checkpw(req["password"].encode(), _user["password"].encode()):
                user = _user
        else:
            if user:
        
                token = { "user": req["email"], "expires": time.mktime((date.today() + timedelta(days=7)).timetuple()) }
                data = LoginResponse(email = dict(user)["email"], token = encodeJWT(token))

                return Response(data = dict(data), code = 200, message="User logged in succesfully")
            else:
                return Response(data = None, code = 404, message="User not found")  
    else:
        return Response(data = None, code = 404, message="User not found")

def doesUserExist() -> Response:
    users: List[User] = db.get(USERS_KEY) or []
    
    if users:
        return Response(data = True, code = 200, message="System user exists")
    else:
        return Response(data = False, code = 200, message="System user does not exist")