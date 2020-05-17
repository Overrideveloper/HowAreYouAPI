from .models import Question
from .request_models import AddEditQuestion as ReqQuestion
from src.constants import QUESTIONS_KEY
from typing import List, Union, Dict
from src.utils import randomInt
from src.response_models import Response
from src.abstract_defs import IDatabase, IProvider

class QuestionProvider(IProvider[Question]):
    db: IDatabase = None
    
    def __init__(self, db: IDatabase):
        self.db = db
        
    def getAll(self) -> Response[List[Question]]:
        data: Dict[str, dict] = self.db.get(QUESTIONS_KEY) or {}
        questions: List[Question] = [Question(**question) for question in data.values()]

        return Response[List[Question]](data = questions, code = 200, message = "{0} Question(s) returned".format(len(questions)))

    def get(self, id: int) -> Union[Response[Question], Response]:
        questions: Dict[str, dict] = self.db.get(QUESTIONS_KEY) or {}
        response: Union[Response[Question], Response] = None
        question: dict = questions.get(str(id))

        if question:
            response = Response[Question](data = Question(**question), code = 200, message = "Question returned")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
        
        return response
        
    def add(self, req: ReqQuestion) -> Response[Question]:
        questions: Dict[str, dict] = self.db.get(QUESTIONS_KEY) or {}
        
        question = Question(question = req.question, defaultAnswer = req.defaultAnswer, id = randomInt())
        questions[str(question.id)] = question.dict()
        
        self.db.set(QUESTIONS_KEY, questions)

        return Response[Question](data = question, code = 201, message = "Question saved")

    def delete(self, id: int) -> Response:
        _id = str(id)
        questions: Dict[str, dict] = self.db.get(QUESTIONS_KEY) or {}
        response: Response = None

        if questions.get(_id):
            questions.pop(_id)
            self.db.set(QUESTIONS_KEY, questions)

            response = Response(data = None, code = 200, message = "Question deleted")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
        
        return response

    def edit(self, id: int, req: ReqQuestion) -> Union[Response[Question], Response]:
        _id = str(id)
        questions: Dict[str, dict] = self.db.get(QUESTIONS_KEY) or {}
        response: Union[Response[Question], Response] = None
        
        if questions.get(_id):
            questions[_id]["question"] = req.question
            questions[_id]["defaultAnswer"] = req.defaultAnswer

            self.db.set(QUESTIONS_KEY, questions)
                    
            response = Response[Question](data = Question(**questions.get(_id)), code = 200, message = "Question modified")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
    
        return response