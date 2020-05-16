from tests.unit.mocks import DatabaseMock
from src.constants import ANSWERS_KEY, QUESTIONS_KEY
from src.modules.answer import AnswerProvider, Answer, AddAnswer, EditAnswer
from src.modules.question import Question
from src.response_models import Response
from typing import List
from src.abstract_defs import IDatabase
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

        payload = AddAnswer(question_id = 99, answer = "For sure")
        
        res = self.answerProvider.add(payload)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
        self.dbMock.remove(QUESTIONS_KEY)
    
    def test_add_403(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        payload = AddAnswer(question_id = 1, answer = "For sure")
        
        res = self.answerProvider.add(payload)
        
        assert isinstance(res, Response)
        assert res.code == 403
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
        self.dbMock.remove(QUESTIONS_KEY)
    
    def test_add_201(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        self.dbMock.set(QUESTIONS_KEY, deepcopy(self.question_list))

        payload = AddAnswer(question_id = 3, answer = "For sure")
        
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
        
        payload = EditAnswer(answer = "No way")
        
        res = self.answerProvider.edit(99, payload)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ANSWERS_KEY)
        
    def test_edit_200(self):
        self.dbMock.set(ANSWERS_KEY, deepcopy(self.answer_list))
        
        payload = EditAnswer(answer = "No way")
        
        res = self.answerProvider.edit(1, payload)
        res1 = self.answerProvider.get(1)
        
        assert isinstance(res, Response)
        assert res.code == 200
        assert res.data.id == 1
        assert res.data.answer == payload.answer

        assert res1.code == 200
        assert res1.data.id == 1
        assert res1.data.answer == payload.answer
        
        self.dbMock.remove(ANSWERS_KEY)
 