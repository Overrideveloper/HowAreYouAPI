from fastapi import APIRouter, Response as HttpResponse
from src.response_models import Response
from typing import Dict
from src.answers.request_models import AddEditAnswer as Answer
import src.answers.provider as provider

answers = APIRouter()

@answers.get('/', response_model = Response, status_code = 200)
def getAnswers():
    return provider.getAnswers()

@answers.get('/{id}', response_model = Response, status_code = 200)
def getAnswer(id: int, response: HttpResponse):
    data: Response = provider.getAnswer(id)
    response.status_code = data["code"]
    return data

@answers.post('/', response_model = Response, status_code = 201)
def addAnswer(payload: Answer, response: HttpResponse):
    data: Response = provider.addAnswer(dict(payload))
    response.status_code = data["code"]
    return data

@answers.delete('/{id}', response_model = Response, status_code = 200)
def deleteAnswer(id: int, response: HttpResponse):
    data: Response = provider.deleteAnswer(id)
    response.status_code = data["code"]
    return data
    
@answers.put('/{id}', response_model = Response, status_code = 200)
def editAnswer(id: int, payload: Answer, response: HttpResponse):
    data: Response = provider.editAnswer(id, dict(payload))
    response.status_code = data["code"]
    return data
    