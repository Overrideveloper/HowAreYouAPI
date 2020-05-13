from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from src.modules.user.models import TokenPayload
from src.jwt.encode_decode import decodeJWT
from datetime import date
from src.constants import USERS_KEY
from typing import List
from src.abstract_defs import IDatabase
import time

class JWTBearer(HTTPBearer):
    db: IDatabase = None
    def __init__(self, db: IDatabase, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.db = db
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code = 401, detail = "You are not authorized to access this resource")
            
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code = 401, detail = "You are not authorized to access this resource")
            
            return credentials.credentials
        else:
            raise HTTPException(status_code = 401, detail = "You are not authorized to access this resource")
    
    def verify_jwt(self, jwtoken: str) -> bool:
        payload: TokenPayload = None
        isTokenValid: bool = False

        try:
            payload = TokenPayload(**decodeJWT(jwtoken))
        except:
            payload = None

        if payload:
            if time.mktime(date.today().timetuple()) > payload.expires:
                pass
            else:
                users: List[dict] = self.db.get(USERS_KEY) or []
                user: dict = None
                
                for _user in users:
                    if _user["email"] == payload.user:
                        user = _user
                else:       
                    if user:
                        isTokenValid = True
        
        return isTokenValid
        