from fastapi.testclient import TestClient
from src import app
from src.response_models import Response
import os

URL_FRAGMENT = "/api/answer"

class Test4_AnswerEndpoints:
    client = TestClient(app)

    def test_get_answers_empty(self, user_data):
        token = user_data[0]
        res = self.client.get(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert len(res.json()["data"]) == 0
    
    def test_get_answer_not_found(self, user_data):
        token = user_data[0]
        res = self.client.get(f"{URL_FRAGMENT}/8375", headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Answer not found").dict()
     
    def test_create_answer_question_not_found(self, user_data):
        token = user_data[0]
        res = self.client.post(URL_FRAGMENT, json={ "question_id": 9243, "answer": "I am well"}, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Question not found").dict()
    
    def test_create_answer_successful(self, user_data, question_ids):
        token = user_data[0]
        question_id = question_ids[0]
        
        res = self.client.post(URL_FRAGMENT, json={ "question_id": question_id, "answer": "I am well"}, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 201
        assert res.json()["data"]["question_id"] == question_id
        assert res.json()["data"]["answer"] == "I am well"
        
    def test_create_answer_question_already_answered(self, user_data, question_ids):
        token = user_data[0]
        question_id = question_ids[0]

        res = self.client.post(URL_FRAGMENT, json={ "question_id": question_id, "answer": "I am not well"}, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 403
        assert res.json() == Response(data = None, code = 403, message = "Question already answered").dict()

    def test_get_answers(self, user_data):
        token = user_data[0]
        res = self.client.get(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert len(res.json()["data"]) == 1
    
    def test_get_answer_successful(self, user_data, answer_id):
        token = user_data[0]
        res = self.client.get(f"{URL_FRAGMENT}/{answer_id}", headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert res.json()["data"]["id"] == answer_id

    def test_edit_answer_not_found(self, user_data):
        token = user_data[0]
        res = self.client.put(f"{URL_FRAGMENT}/8375", json={ "answer": "I am very well" }, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Answer not found").dict()

    def test_edit_answer_successful(self, user_data, answer_id):
        token = user_data[0]
        res = self.client.put(f"{URL_FRAGMENT}/{answer_id}", json={ "answer": "I am very well" }, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 200
        assert res.json()["message"] == "Answer modified"
        assert res.json()["data"]["id"] == answer_id
        assert res.json()["data"]["answer"] == "I am very well"

    def test_delete_answer_not_found(self, user_data):
        token = user_data[0]
        res = self.client.delete(f"{URL_FRAGMENT}/8375", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Answer not found").dict()

    def test_delete_successful(self, user_data, answer_id):
        token = user_data[0]
        res = self.client.delete(f"{URL_FRAGMENT}/{answer_id}", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code == 200
        assert res.json() == Response(data = None, code = 200, message = "Answer deleted").dict()
    