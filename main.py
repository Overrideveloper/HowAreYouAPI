from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.exceptions_handlers import validationExceptionHandler, httpExceptionHandler
from src.modules.answer.routes import answerRouter
from src.modules.question.routes import questionRouter
from src.modules.address.routes import addressRouter
from src.modules.user.routes import userRouter
from src.jwt.jwt_bearer import JWTBearer
from src.scheduler.cron import schedule
from src.response_models import Response
from src.modules.email_log.models import EmailLog
from src.db import Database
from src.modules.email_log.provider import EmailLogProvider
from typing import Dict

app = FastAPI()
jwt_bearer = JWTBearer(Database())
emailLogProvider = EmailLogProvider(Database())

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
    return emailLogProvider.getTodaysLog()

app.include_router(answerRouter, prefix="/api/answer", tags=["Answer"], dependencies=[Depends(jwt_bearer)])
app.include_router(questionRouter, prefix="/api/question", tags=["Question"], dependencies=[Depends(jwt_bearer)])
app.include_router(addressRouter, prefix="/api/address", tags=["Address"], dependencies=[Depends(jwt_bearer)])
app.include_router(userRouter, prefix="/api/auth", tags=["Auth"])