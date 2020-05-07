from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.utils import validationExceptionHandler, jwtValidationHandler
from src.answer.routes import answer
from src.question.routes import question
from src.address.routes import address
from src.user.routes import user
from src.cron import schedule

import src.email_log.provider as logProvider

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

@app.middleware('http')
def validate_jwt(request: Request, call_next):
    return jwtValidationHandler(request, call_next)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    return validationExceptionHandler(exc)

@app.on_event("startup")
def startup():
    pass
    # schedule()
    
@app.get('/')
def index():
    return { "description": "HowAreYou Service API" }


@app.get('/api/log/today')
def getTodaysEmailLog():
    return logProvider.getTodaysLog()

app.include_router(answer, prefix="/api/answer", tags=["answer"])
app.include_router(question, prefix="/api/question", tags=["question"])
app.include_router(address, prefix="/api/address", tags=["address"])
app.include_router(user, prefix="/api/user", tags=["user"])