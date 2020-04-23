from typing import Any
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import random
import re

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
    
    errorMsg = f"{errorCount} validation errors for this request: {str(errorValues)}"
    
    return JSONResponse(content={ "data": errorList, "code": 400, "message": errorMsg }, status_code=400)