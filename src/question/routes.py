from fastapi import APIRouter, Response as HttpResponse
from src.response_models import Response
from src.question.request_models import AddEditQuestion as Question
import src.question.provider as provider

question = APIRouter()

@question.get('/', response_model = Response, status_code = 200)
def getQuestions():
    return provider.getQuestions()

@question.get('/{id}', response_model = Response, status_code = 200)
def getQuestion(id: int, response: HttpResponse):
    data: Response = provider.getQuestion(id)
    response.status_code = data["code"]
    return data

@question.post('/', response_model = Response, status_code = 201)
def addQuestion(payload: Question):
    data: Response = provider.addQuestion(dict(payload))
    return data

@question.delete('/{id}', response_model = Response, status_code = 200)
def deleteQuestion(id: int, response: HttpResponse):
    data: Response = provider.deleteQuestion(id)
    response.status_code = data["code"]
    return data

@question.put('/{id}', response_model = Response, status_code = 200)
def editQuestion(id: int, payload: Question, response: HttpResponse):
    data: Response = provider.editQuestion(id, dict(payload))
    response.status_code = data["code"]
    return data