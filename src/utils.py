from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.constants import JWT_SECRET
from src.response_models import Response
from src.user.request_models import TokenPayload
from datetime import date, timedelta
import time
import random
import re
import jwt

def randomInt() -> int:
    return random.randint(1000, 9999)

def validateEmail(email: str) -> bool:
    if (re.match("^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$", email) != None):
        return True
    return False

def validationExceptionHandler(exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    errorCount = len(errors)
    errorList: list = []
    errorValues: list = []
    
    for i in range(errorCount):
        errorValue = errors[i]["loc"][len(errors[i]["loc"]) - 1]
        errorList.append(errors[i]["msg"].replace("value", errorValue))
        errorValues.append(errorValue)
    
    errorMsg = f"{errorCount} validation error{'s' if not errorCount or errorCount > 1 else ''} for this request: {str(errorValues)}"
    
    return JSONResponse(content={ "data": errorList, "code": 400, "message": errorMsg }, status_code=400)

def encodeJWT(payload: dict) -> str:
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256").decode()

def decodeJWT(token: str) -> dict:
    try:
        return jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
    except:
        return None

async def jwtValidationHandler(request: Request, call_next):
    req = dict(request)
    unauth_res = Response(code=401, data=None, message="You are not authorized to access this resource")

    if req["path"].find("api/user") > -1 or req["path"] == "/":
        response = await call_next(request)
    else:
        for header in req["headers"]:
            if header[0].decode() == "auth_token":
                token = header[1].decode()
        else:    
            if token:
                try:
                    payload = TokenPayload(**decodeJWT(token))
                except:
                    payload = None

                if payload:
                    if time.mktime(date.today().timetuple()) > payload.expires:
                        response = JSONResponse(content = dict(unauth_res), status_code = 401)
                    else:
                        response = await call_next(request)
                else:
                    response = JSONResponse(content = dict(unauth_res), status_code = 401)
            else:
                response = JSONResponse(content = dict(unauth_res), status_code = 401)

    return response