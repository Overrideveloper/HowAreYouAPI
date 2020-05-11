import src.email as email_sender

from src.response_models import Response
from src.question.models import Question
from src.answer.models import Answer
from src.address.models import Address
from src.constants import SUBJECT_NAME
from src.email_templates import genDailyAnswerBlock, genDailyAnswers
from src.db import Database
from src.address.provider import AddressProvider
from src.email_log.provider import EmailLogProvider
from src.question.provider import QuestionProvider
from src.answer.provider import AnswerProvider

from typing import List, Union

questionProvider = QuestionProvider(Database())
logProvider = EmailLogProvider(Database())
addressProvider = AddressProvider(Database())
answerProvider = AnswerProvider(Database())


def SEND_EMAIL_TO_ADDRESSES():
    questionRes: Response[List[Question]] = questionProvider.getAll()
    addressRes: Response[List[Address]] = addressProvider.getAll()
    answerRes: Response[List[Answer]] = answerProvider.getAll()

    if questionRes.code == 200 and addressRes.code == 200 and answerRes.code == 200:
        questions: List[Question] = questionRes.data
        addresses: List[Address] = addressRes.data
        _answers: List[Answer] = answerRes.data

        answers = ""
        
        for question in questions:
            answer = None

            for _answer in _answers:
                if _answer.question_id == question.id:
                    answer = _answer.answer
            else:
                answers += genDailyAnswerBlock(question.question, answer if answer else question.defaultAnswer)
        else:
            successCount = 0

            for address in addresses:
                res = email_sender.sendMail(email_sender.createMail(address.email, f"How {SUBJECT_NAME} is doing today", genDailyAnswers(address.name, answers)))
                
                successCount += 1 if res else 0
            else:
                logProvider.addTodayLog(successCount)

def RESET_ANSWERS():
    answerProvider.deleteAll()