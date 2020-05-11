from fastapi import APIRouter, Path, Body
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.question.request_models import AddEditQuestion as ReqQuestion
from src.question.models import Question
from typing import List, Union
from src.utils import generate404ResContent, generate400ResContent
from src.db import Database
from src.question.provider import QuestionProvider

question = APIRouter()
questionProvider = QuestionProvider(Database())

@question.get('/', summary="Get Questions", description="Get a list of all questions", response_model=Response[List[Question]])
def getQuestions():
    data: Response[List[Question]] = questionProvider.getAll()

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.get('/{id}', summary="Get Question", description="Get a question", response_model=Response[Question],
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 422: {} })
def getQuestion(id: int = Path(..., gt=0, description="The ID of the question to get")):
    data: Union[Response[Question], Response] = questionProvider.get(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.post('/', summary="Add Question", description="Create and save a question", response_model=Response[Question],
responses={ 400: generate400ResContent(), 422: {} })
def addQuestion(payload: ReqQuestion = Body(..., description="The question to create")):
    data: Union[Response[Question], Response] = questionProvider.add(payload)

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.delete('/{id}', summary="Delete Question", description="Delete a question", response_model=Response,
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 422: {} })
def deleteQuestion(id: int = Path(..., gt=0, description="The ID of the question to delete")):
    data: Response = questionProvider.delete(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@question.put('/{id}', summary="Edit Question", description="Edit a question", response_model=Response[Question],
responses={ 404: generate404ResContent("Question"), 400: generate400ResContent(), 422: {} })
def editQuestion(id: int = Path(..., gt=0, description="The ID of the question to edit"), payload: ReqQuestion = Body(..., description="The question data to be used in the edit")):
    data: Union[Response[Question], Response] = questionProvider.edit(id, payload)

    return JSONResponse(content = data.dict(), status_code = data.code)