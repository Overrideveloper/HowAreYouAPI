from fastapi import APIRouter, Path, Body
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.modules.answer.request_models import AddAnswer, EditAnswer
from src.modules.answer.models import Answer
from typing import List, Union
from src.utils import generate404ResContent, generate400ResContent, generate403ResContent
from src.db import Database
from src.modules.answer.provider import AnswerProvider

answerRouter = APIRouter()
answerProvider = AnswerProvider(Database())

@answerRouter.get('', summary="Get Answers", description="Get a list of all answers", response_model=Response[List[Answer]])
def getAnswers():
    data: Response[List[Answer]] = answerProvider.getAll()

    return JSONResponse(content = data.dict(), status_code = data.code)

@answerRouter.get('/{id}', summary="Get Answer", description="Get an answer", response_model=Response[Answer],
responses={ 404: generate404ResContent("Answer"), 400: generate400ResContent(), 422: {} })
def getAnswer(id: int = Path(..., gt=0, description="The ID of the answer to get")):
    data: Union[Response[Answer], Response] = answerProvider.get(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@answerRouter.post('', summary="Add Answer", description="Create and save an answer to a question", status_code=201, response_model=Response[Answer],
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 403: generate403ResContent("Question already answered"), 422: {} })
def addAnswer(payload: AddAnswer = Body(..., description="The answer to create")):
    data: Union[Response[Answer], Response] = answerProvider.add(payload)

    return JSONResponse(content = data.dict(), status_code = data.code)

@answerRouter.delete('/{id}', summary="Delete Answer", description="Delete an answer", response_model=Response,
responses={ 404: generate404ResContent("Answer"), 400: generate400ResContent(), 422: {} })
def deleteAnswer(id: int = Path(..., gt=0, description="The ID of the answer to delete")):
    data: Response = answerProvider.delete(id)

    return JSONResponse(content = data.dict(), status_code = data.code)
    
@answerRouter.put('/{id}', summary="Edit Answer", description="Edit an answer", response_model=Response[Answer],
responses={ 404: generate404ResContent("Answer"), 400: generate400ResContent(), 422: {} })
def editAnswer(id: int = Path(..., gt=0, description="The ID of the answer to edit"), payload: EditAnswer = Body(..., description="The answer data to be used in the edit")):
    data: Union[Response[Answer], Response] = answerProvider.edit(id, payload)

    return JSONResponse(content = data.dict(), status_code = data.code)
