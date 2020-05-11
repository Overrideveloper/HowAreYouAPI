from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.exceptions_handlers import validationExceptionHandler, httpExceptionHandler
from src.answer.routes import answer
from src.question.routes import question
from src.address.routes import address
from src.user.routes import user
from src.jwt.jwt_bearer import JWTBearer
from src.cron import schedule
from src.response_models import Response
from src.email_log.models import EmailLog
from typing import Dict

import src.email_log.provider as logProvider

app = FastAPI()
jwt_bearer = JWTBearer()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return validationExceptionHandler(exc)

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return httpExceptionHandler(request, exc)

@app.on_event("startup")
def startup():
    pass
    # schedule()
    
@app.get('/', tags=["Index"], response_model=Dict[str, str])
def index():
    return { "description": "HowAreYou Service API" }


@app.get('/api/log/today', tags=["Email Log"], summary="Get Today's Email Log", description="Get email log information for today.", response_model=Response[EmailLog],
dependencies=[Depends(jwt_bearer)])
def getTodaysEmailLog():
    return logProvider.getTodaysLog()

app.include_router(answer, prefix="/api/answer", tags=["Answer"], dependencies=[Depends(jwt_bearer)])
app.include_router(question, prefix="/api/question", tags=["Question"], dependencies=[Depends(jwt_bearer)])
app.include_router(address, prefix="/api/address", tags=["Address"], dependencies=[Depends(jwt_bearer)])
app.include_router(user, prefix="/api/auth", tags=["Auth"])