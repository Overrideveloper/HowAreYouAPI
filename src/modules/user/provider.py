from src.constants import USERS_KEY
from src.utils import randomInt, randomAlphanumericStr
from src.jwt import encodeJWT
from src.response_models import Response
from .models import User, TokenPayload
from .response_models import LoginResponse
from .request_models import SignupLoginUser as UserReq, ChangePassword, ResetPassword
from typing import List, Union, Dict
from datetime import date, timedelta
from src.email import genPasswordResetEmail, EmailHelper
from src.abstract_defs import IDatabase, IEmailHelper
import time
import bcrypt

class UserProvider():
    db: IDatabase = None
    emailHelper: IEmailHelper = None
    
    def __init__(self, db: IDatabase, emailHelper: IEmailHelper):
        self.db = db
        self.emailHelper = emailHelper

    def signup(self, req: UserReq) -> Union[Response[LoginResponse], Response]:
        users: Dict[str, dict] = self.db.get(USERS_KEY) or {}
        response: Union[Response[LoginResponse], Response] = None
        
        if len(users):
            response = Response(data = None, code = 403, message="This is a one-user system and a user already exists.")
        else:
            user = User(id=randomInt(), email=req.email, password=bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode())

            users[str(user.id)] = user.dict()
            self.db.set(USERS_KEY, users)
            
            token = TokenPayload(user_id = user.id, expires = time.mktime((date.today() + timedelta(days=7)).timetuple()), randomizer = randomInt())
            loginRes = LoginResponse(id = user.id, email = user.email, token = encodeJWT(token.dict()))

            response = Response[LoginResponse](data = loginRes, code = 201, message="User signed up successfully")
        
        return response

    def login(self, req: UserReq) -> Union[Response[LoginResponse], Response]:
        users: Dict[str, dict] = self.db.get(USERS_KEY) or {}
        response: Union[Response[LoginResponse], Response] = None

        user: dict = None

        for _user in users.values():
            if req.email == _user["email"] and bcrypt.checkpw(req.password.encode(), _user["password"].encode()):
                user = _user
        else:
            if user:
                token = TokenPayload(user_id = user["id"], expires = time.mktime((date.today() + timedelta(days=7)).timetuple()), randomizer = randomInt())
                loginRes = LoginResponse(id = user["id"], email = user["email"], token = encodeJWT(token.dict()))

                response = Response[LoginResponse](data = loginRes, code = 200, message="User logged in succesfully")
            else:
                response = Response(data = None, code = 404, message="User not found")  

        return response

    def changePassword(self, id: int, req: ChangePassword) -> Union[Response[bool], Response]:
        _id = str(id)
        users: Dict[str, dict] = self.db.get(USERS_KEY) or {}
        response: Union[Response[bool], Response] = None

        user = users.get(_id) if users.get(_id) and bcrypt.checkpw(req.old_password.encode(), users.get(_id)["password"].encode()) else None

        if user:
            user["password"] = bcrypt.hashpw(req.new_password.encode(), bcrypt.gensalt()).decode()
            users[_id] = user

            self.db.set(USERS_KEY, users)

            response = Response[bool](data = True, code = 200, message="User password changed succesfully")
        else:
            response = Response(data = None, code = 404, message="User not found")  

        return response

    def resetPassword(self, req: ResetPassword) -> Union[Response[bool], Response]:
        users: Dict[str, dict] = self.db.get(USERS_KEY) or {}
        response: Union[Response[bool], Response] = None

        id: str = None

        for user in users.items():
            if req.email == user[1]["email"]:
                id = user[0]
        else:
            if id:
                new_password = randomAlphanumericStr(6)
                users[id]["password"] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

                self.db.set(USERS_KEY, users)
                
                self.emailHelper.sendMail(self.emailHelper.createMail(req.email, "Your password has been reset", genPasswordResetEmail(new_password)))

                response = Response[bool](data = True, code = 200, message="Password reset succesfully. New auto-generated password sent to email.")
            else:
                response = Response(data = None, code = 404, message="User not found")

        return response

    def doesUserExist(self) -> Response[bool]:
        users: Dict[str, dict] = self.db.get(USERS_KEY) or {}
        response: Response[bool] = None
        
        if len(users):
            response = Response[bool](data = True, code = 200, message="System user exists")
        else:
            response = Response[bool](data = False, code = 200, message="System user does not exist")
        
        return response