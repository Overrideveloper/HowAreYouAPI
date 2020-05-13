from tests.unit.mocks.db_mock import DatabaseMock
from src.modules.answer.provider import AnswerProvider
from src.response_models import Response
from src.modules.answer.models import Answer
from src.modules.question.models import Question
from typing import List
from src.abstract_defs import IDatabase
from src.constants import ANSWERS_KEY, QUESTIONS_KEY
from src.modules.answer.request_models import AddEditAnswer
from copy import deepcopy

class TestAnswerProvider():
    dbMock: IDatabase = DatabaseMock()
    answerProvider: AnswerProvider = AnswerProvider(dbMock)
    answer_list: List[dict] = list([
        Answer(id = 1, answer = "Yes", question_id = 1).dict(),
        Answer(id = 2, answer = "No", question_id = 2).dict(),
    ])
    question_list: List[dict] = list([
        Question(id = 1, question = "Hello?", defaultAnswer = "Hi").dict(),
        Question(id = 2, question = "How are you?", defaultAnswer = "Fine").dict(),
        Question(id = 3, question = "How do you do?", defaultAnswer = "Well").dict()
    ])
    
    def test_creation(self):
        assert self.answerProvider is not None
    
    def test_get_all_empty(self):
        res = self.answerProvider.getAll()
        
        assert isinstance(res, Response[List[Answer]])
        assert res.code == 200
        assert len(res.data) == 0
        
    def test_get_all_non_empty(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))

        res = self.answerProvider.getAll()
        
        assert isinstance(res, Response[List[Answer]])
        assert res.code == 200
        assert len(res.data) == len(self.answer_list)
        
        self.dbMock.remove(ANSWERS_KEY)
        
    def test_get_200(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))

        res = self.answerProvider.get(1)
        
        assert isinstance(res, Response[Answer])
        assert res.code == 200
        assert isinstance(res.data, Answer)
        assert res.data.dict() == self.answer_list[0]
        
        self.dbMock.remove(ANSWERS_KEY)
        
    def test_get_404(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))

        res = self.answerProvider.get(99)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
   
    def test_add_404(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        payload = AddEditAnswer(question_id = 99, answer = "For sure")
        
        res = self.answerProvider.add(payload)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
        self.dbMock.remove(QUESTIONS_KEY)
    
    def test_add_403(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        payload = AddEditAnswer(question_id = 1, answer = "For sure")
        
        res = self.answerProvider.add(payload)
        
        assert isinstance(res, Response)
        assert res.code == 403
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
        self.dbMock.remove(QUESTIONS_KEY)
    
    def test_add_201(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        payload = AddEditAnswer(question_id = 3, answer = "For sure")
        
        res = self.answerProvider.add(payload)
        
        assert isinstance(res, Response[Answer])
        assert res.code == 201
        assert isinstance(res.data, Answer)
        assert res.data == Answer(id = res.data.id, **payload.dict()).dict()

        self.dbMock.remove(ANSWERS_KEY)
        self.dbMock.remove(QUESTIONS_KEY)

    def test_delete_404(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        
        res = self.answerProvider.delete(99)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
    
    def test_delete_200(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))

        res = self.answerProvider.delete(1)
        res1 = self.answerProvider.getAll()
        
        assert isinstance(res, Response)
        assert res.code == 200

        assert res1.code == 200
        assert len(res1.data) == 1
        assert res1.data[0] == self.answer_list[1]

        self.dbMock.remove(ANSWERS_KEY)

    def test_edit_404(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        
        payload = AddEditAnswer(answer = "No way", question_id = 1)
        
        res = self.answerProvider.edit(99, payload)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)

    def test_edit_404_1(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))
        
        payload = AddEditAnswer(answer = "No way", question_id = 99)
        
        res = self.answerProvider.edit(1, payload)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
        self.dbMock.remove(QUESTIONS_KEY)
        
    def test_edit_200(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))
        
        payload = AddEditAnswer(answer = "No way", question_id = 1)
        
        res = self.answerProvider.edit(1, payload)
        res1 = self.answerProvider.get(1)
        
        assert isinstance(res, Response)
        assert res.code == 200
        assert res.data == Answer(id = 1, **payload.dict()).dict()

        assert res1.code == 200
        assert res1.data == Answer(id = 1, **payload.dict())
        
        self.dbMock.remove(ANSWERS_KEY)
        self.dbMock.remove(QUESTIONS_KEY)
 