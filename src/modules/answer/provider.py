from .models import Answer
from .request_models import AddAnswer, EditAnswer
from src.modules.question import Question
from src.constants import ANSWERS_KEY, QUESTIONS_KEY
from src.utils import randomInt
from src.response_models import Response
from typing import List, Union, Dict
from src.abstract_defs import IDatabase, IProvider

class AnswerProvider(IProvider[Answer]):
    db: IDatabase = None
    
    def __init__(self, db: IDatabase):
        self.db = db

    def getAll(self) -> Response[List[Answer]]:
        data: Dict[str, dict] = self.db.get(ANSWERS_KEY) or {}
        answers: List[Answer] = [Answer(**answer) for answer in data.values()]

        return Response[List[Answer]](data = answers, code = 200, message = "{0} Answer(s) returned".format(len(answers)))

    def get(self, id: int) -> Union[Response[Answer], Response]:
        answers: Dict[str, dict] = self.db.get(ANSWERS_KEY) or {}
        response: Union[Response[Answer], Response] = None
        answer: dict = answers.get(str(id))
        
        if answer:
            response = Response[Answer](data = Answer(**answer), code = 200, message = "Answer returned")
        else:
            response = Response(data = None, code = 404, message = "Answer not found")
        
        return response
        
    def add(self, req: AddAnswer) -> Union[Response[Answer], Response]:
        questions: Dict[str, dict] = self.db.get(QUESTIONS_KEY) or {}
        response: Union[Response[Answer], Response] = None

        if questions.get(str(req.question_id)):
            answers: Dict[str, dict] = self.db.get(ANSWERS_KEY) or {}
            question_already_answered: bool = False
            
            for answ in answers.values():
                if answ["question_id"] == req.question_id:
                    question_already_answered = True
            else:
                if not question_already_answered:
                    answer = Answer(answer = req.answer, question_id = req.question_id, id = randomInt())
                    answers[str(answer.id)] = answer.dict()

                    self.db.set(ANSWERS_KEY, answers)

                    response = Response[Answer](data = answer, code = 201, message = "Answer saved")
                else:
                    response = Response(data = None, code = 403, message = "Question already answered")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
        
        return response
    
    def delete(self, id: int) -> Response:
        _id = str(id)
        answers: Dict[str, dict] = self.db.get(ANSWERS_KEY) or {}
        response: Response = None

        if answers.get(_id):
            answers.pop(_id)
            self.db.set(ANSWERS_KEY, answers)

            response = Response(data = None, code = 200, message = "Answer deleted")
        else:
            response = Response(data = None, code = 404, message = "Answer not found")
        
        return response

    def edit(self, id: int, req: EditAnswer) -> Union[Response[Answer], Response]:
        _id = str(id)
        answers: Dict[str, dict] = self.db.get(ANSWERS_KEY) or {}
        response: Union[Response[Answer], Response] = None

        if answers.get(_id):
            answers[_id]["answer"] = req.answer
            self.db.set(ANSWERS_KEY, answers)
            
            response = Response[Answer](data = Answer(**answers.get(_id)), code = 200, message = "Answer modified")
        else:
            response = Response(data = None, code = 404, message = "Answer not found")
    
        return response

    def deleteAll(self):
        self.db.remove(ANSWERS_KEY)