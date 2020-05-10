from fastapi import APIRouter, Path, Body
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.answer.request_models import AddEditAnswer as ReqAnswer
from src.answer.models import Answer
import src.answer.provider as provider
from typing import List, Union
from src.utils import generate404ResContent, generate400ResContent, generate403ResContent

answer = APIRouter()

@answer.get('/', summary="Get Answers", description="Get a list of all answers", response_model=Response[List[Answer]])
def getAnswers():
    data: Response[List[Answer]] = provider.getAnswers()

    return JSONResponse(content = data.dict(), status_code = data.code)

@answer.get('/{id}', summary="Get Answer", description="Get an answer", response_model=Response[Answer],
responses={ 404: generate404ResContent("Answer"), 400: generate400ResContent(), 422: {} })
def getAnswer(id: int = Path(..., description="The ID of the answer to get")):
    data: Union[Response[Answer], Response] = provider.getAnswer(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@answer.post('/', summary="Add Answer", description="Create and save an answer to a question", status_code=201, response_model=Response[Answer],
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 403: generate403ResContent("Question already answered"), 422: {} })
def addAnswer(payload: ReqAnswer = Body(..., description="The answer to create")):
    data: Union[Response[Answer], Response] = provider.addAnswer(payload)

    return JSONResponse(content = data.dict(), status_code = data.code)

@answer.delete('/{id}', summary="Delete Answer", description="Delete an answer", response_model=Response,
responses={ 404: generate404ResContent("Answer"), 400: generate400ResContent(), 422: {} })
def deleteAnswer(id: int = Path(..., description="The ID of the answer to delete")):
    data: Response = provider.deleteAnswer(id)

    return JSONResponse(content = data.dict(), status_code = data.code)
    
@answer.put('/{id}', summary="Edit Answer", description="Edit an answer", response_model=Response[Answer],
responses={ 404: generate404ResContent("Answer"), 400: generate400ResContent(), 422: {} })
def editAnswer(id: int = Path(..., description="The ID of the answer to edit"), payload: ReqAnswer = Body(..., description="The answer data to be used in the edit")):
    data: Union[Response[Answer], Response] = provider.editAnswer(id, payload)

    return JSONResponse(content = data.dict(), status_code = data.code)
