from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.question.request_models import AddEditQuestion as Question
import src.question.provider as provider

question = APIRouter()

@question.get('/')
def getQuestions():
    data: Response = provider.getQuestions()
    return JSONResponse(content=data, status_code=data["code"])

@question.get('/{id}')
def getQuestion(id: int):
    data: Response = provider.getQuestion(id)
    return JSONResponse(content=data, status_code=data["code"])

@question.post('/')
def addQuestion(payload: Question):
    data: Response = provider.addQuestion(dict(payload))
    return JSONResponse(content=data, status_code=data["code"])

@question.delete('/{id}')
def deleteQuestion(id: int):
    data: Response = provider.deleteQuestion(id)
    return JSONResponse(content=data, status_code=data["code"])

@question.put('/{id}')
def editQuestion(id: int, payload: Question):
    data: Response = provider.editQuestion(id, dict(payload))
    return JSONResponse(content=data, status_code=data["code"])