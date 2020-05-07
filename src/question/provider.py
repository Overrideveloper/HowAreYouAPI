from src.question.models import Question
from src.question.request_models import AddEditQuestion as ReqQuestion
from src.constants import QUESTIONS_KEY
from typing import List
from src.utils import randomInt
import src.db as db
from src.response_models import Response
    
def getQuestions() -> Response:
    data: List[dict] = db.get(QUESTIONS_KEY) or []
    return Response(data = data, code = 200, message = "{0} Question(s) returned".format(len(data)))

def getQuestion(id: int) -> Response:
    questions: List[dict] = db.get(QUESTIONS_KEY) or []
    response: Response = None
    question: dict = None
    
    for ques in questions:
        if ques["id"] == id:
            question = ques
    else:
        if question:
            response = Response(data = question, code = 200, message = "Question returned")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
    
    return response
    
def addQuestion(req: ReqQuestion) -> Response:
    questions: List[dict] = db.get(QUESTIONS_KEY) or []
    
    question = Question(question = req.question, defaultAnswer = req.defaultAnswer, id = randomInt())
    
    questions.append(dict(question))
    db.set(QUESTIONS_KEY, questions)

    return Response(data = dict(question), code = 200, message = "Question saved")

def deleteQuestion(id: int) -> Response:
    questions: List[dict] = db.get(QUESTIONS_KEY) or []
    response: Response = None
    question_index: int = None
    
    for i in range(len(questions)):
        if questions[i]["id"] == id:
            question_index = i
    else:
        if question_index is not None:
            del questions[question_index]
            db.set(QUESTIONS_KEY, questions)

            response = Response(data = None, code = 200, message = "Question deleted")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
    
    return response

def editQuestion(id: int, req: ReqQuestion) -> Response:
    questions: List[dict] = db.get(QUESTIONS_KEY) or []
    response: Response = None
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
            db.set(QUESTIONS_KEY, questions)
                    
            response = Response(data = question, code = 200, message = "Question modified")
        else:
            response = Response(data = None, code = 404, message = "Question not found")
    
    return response