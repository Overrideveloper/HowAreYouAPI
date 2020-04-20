from src.answers.models import Answer
from src.questions.models import Question
from src.constants import ANSWERS_KEY, QUESTIONS_KEY
from src.utils import randomInt
from typing import List, Dict
from src.utils import randomInt
import src.db as db

def getAnswers():
    return db.get(ANSWERS_KEY) or []

def getAnswer(id: int):
    answers: List[Answer] = db.get(ANSWERS_KEY) or []
    answer: Answer = None
    
    for a in answers:
        if a["id"] == id:
            answer = a
    else:
        return answer
    
def addAnswer(req: Dict):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question: Question = None
    
    for q in questions:
        if q["id"] == req["question_id"]:
            question = q
    else:
        if question is not None:
            answers: List[Answer] = db.get(ANSWERS_KEY) or []
            answer = dict(Answer(answer = req["answer"], question_id = question["id"], id = randomInt()))
            
            answers.append(answer)
            db.set(ANSWERS_KEY, answers)

            return { "code": 200, "data": answer}
        else:
            return { "code": 404, "message": "Question not found" }
 
def deleteAnswer(id: int):
    answers: List[Answer] = db.get(ANSWERS_KEY) or []
    answer_index = None
    
    for i in range(len(answers)):
        if answers[i]["id"] == id:
            answer_index = i
    else:
        if answer_index is not None: 
            answer = answers[answer_index]

            del answers[answer_index]
            db.set(ANSWERS_KEY, answers)

            return answer
        else:
            return None

def editAnswer(id: int, req: Dict):
    questions: List[Question] = db.get(QUESTIONS_KEY) or []
    question: Question = None
    
    for q in questions:
        if q["id"] == req["question_id"]:
            question = q
    else:
        if question is not None:
            answers: List[Answer] = db.get(ANSWERS_KEY) or []
            answer_index = None
            
            for i in range(len(answers)):
                if answers[i]["id"] == id:
                    answer_index = i
            else:
                if answer_index is not None:
                    answer = answers[answer_index]
                    answer["question_id"] = question["id"]
                    answer["answer"] = req["answer"]
                    
                    del answers[answer_index]

                    answers.insert(answer_index, answer)
                    db.set(ANSWERS_KEY, answers)
                    
                    return { "code": 200, "data": answer }
                else:
                    return { "code": 404, "message": "Answer not found" }
        else:
            return { "code": 404, "message": "Question not found" }
