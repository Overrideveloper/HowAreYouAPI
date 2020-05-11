from src.modules.question.models import Question
from src.modules.question.request_models import AddEditQuestion as ReqQuestion
from src.constants import QUESTIONS_KEY
from typing import List, Union
from src.utils import randomInt
from src.response_models import Response
from src.db import IDatabase
from src.abstract_defs import IProvider

class QuestionProvider(IProvider[Question]):
    db: IDatabase = None
    
    def __init__(self, db: IDatabase):
        self.db = db
        
    def getAll(self) -> Response[List[Question]]:
        data: List[dict] = self.db.get(QUESTIONS_KEY) or []
        return Response[List[Question]](data = data, code = 200, message = "{0} Question(s) returned".format(len(data)))

    def get(self, id: int) -> Union[Response[Question], Response]:
        questions: List[dict] = self.db.get(QUESTIONS_KEY) or []
        response: Union[Response[Question], Response] = None
        question: dict = None
        
        for ques in questions:
            if ques["id"] == id:
                question = ques
        else:
            if question:
                response = Response[Question](data = Question(**question), code = 200, message = "Question returned")
            else:
                response = Response(data = None, code = 404, message = "Question not found")
        
        return response
        
    def add(self, req: ReqQuestion) -> Response[Question]:
        questions: List[dict] = self.db.get(QUESTIONS_KEY) or []
        
        question = Question(question = req.question, defaultAnswer = req.defaultAnswer, id = randomInt())
        
        questions.append(question.dict())
        self.db.set(QUESTIONS_KEY, questions)

        return Response[Question](data = question, code = 200, message = "Question saved")

    def delete(self, id: int) -> Response:
        questions: List[dict] = self.db.get(QUESTIONS_KEY) or []
        response: Response = None
        question_index: int = None
        
        for i in range(len(questions)):
            if questions[i]["id"] == id:
                question_index = i
        else:
            if question_index is not None:
                del questions[question_index]
                self.db.set(QUESTIONS_KEY, questions)

                response = Response(data = None, code = 200, message = "Question deleted")
            else:
                response = Response(data = None, code = 404, message = "Question not found")
        
        return response

    def edit(self, id: int, req: ReqQuestion) -> Union[Response[Question], Response]:
        questions: List[dict] = self.db.get(QUESTIONS_KEY) or []
        response: Union[Response[Question], Response] = None
        question_index: int = None
        
        for i in range(len(questions)):
            if questions[i]["id"] == id:
                question_index = i
        else:
            if question_index is not None:
                question = questions[question_index]
                question["question"] = req.question
                question["defaultAnswer"] = req.defaultAnswer
                
                del questions[question_index]

                questions.insert(question_index, question)
                self.db.set(QUESTIONS_KEY, questions)
                        
                response = Response[Question](data = Question(**question), code = 200, message = "Question modified")
            else:
                response = Response(data = None, code = 404, message = "Question not found")
        
        return response