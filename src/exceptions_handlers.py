from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from src.response_models import Response

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
    data = Response(data = errorList, code = 400, message = errorMsg)

    return JSONResponse(content = data.dict(), status_code = data.code)

def httpExceptionHandler(request: Request, exc: HTTPException):
    data: Response = None
    
    if isinstance(exc.detail, str):
        data = Response(code = exc.status_code, data = None, message = exc.detail)
    else:
        data = Response(code = exc.status_code, data = exc.detail, message = "An error occurred. Please try again.")    
    
    return JSONResponse(content = data.dict(), status_code = data.code)
