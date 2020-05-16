from fastapi.testclient import TestClient
from src import app
from src.response_models import Response
import os

URL_FRAGMENT = "/api/auth"

class Test1_AuthEndpoints:
    client = TestClient(app)
    
    def test_status_false(self):
        res = self.client.get(f"{URL_FRAGMENT}/status")
        
        assert res.status_code == 200
        assert res.json() == Response[bool](data = False, code = 200, message="System user does not exist").dict()

    def test_signup_success(self):
        res = self.client.post(f"{URL_FRAGMENT}/signup", json={ "email": "johndoe@doe.com", "password": "johndoe" })
        
        assert res.status_code == 201
        assert res.json()["data"]["id"]
        assert res.json()["data"]["email"]
        assert res.json()["data"]["token"]
    
    def test_status_true(self):
        res = self.client.get(f"{URL_FRAGMENT}/status")
        
        assert res.status_code == 200
        assert res.json() == Response[bool](data = True, code = 200, message="System user exists").dict()
       
    def test_signup_forbidden(self):
        res = self.client.post(f"{URL_FRAGMENT}/signup", json={ "email": "johndoe@doe.com", "password": "johndoe" })
        
        assert res.status_code == 403
        assert res.json() == Response(data = None, code = 403, message="This is a one-user system and a user already exists.").dict()

    def test_login_user_not_found(self):
        res = self.client.post(f"{URL_FRAGMENT}/login", json={ "email": "mary@poppins.com", "password": "marypoppins" })
        
        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "User not found").dict()
        
    def test_login_success(self):
        res = self.client.post(f"{URL_FRAGMENT}/login", json={ "email": "johndoe@doe.com", "password": "johndoe" })
        
        assert res.status_code == 200
        assert res.json()["data"]["id"]
        assert res.json()["data"]["email"]
        assert res.json()["data"]["token"]
        
        os.environ["TEST_USER_ID"] = str(res.json()["data"]["id"])
        os.environ["TEST_TOKEN"] = res.json()["data"]["token"]
    
    def test_change_password_unauthorized(self):
        user_id = int(os.environ.get("TEST_USER_ID"))
        res = self.client.put(f"{URL_FRAGMENT}/change-password/{user_id}", json={ "old_password": "johndoe", "new_password": "johndeux" })
        
        assert res.status_code == 403
        assert res.json() == Response(data = None, code = 403, message = "Not authenticated").dict()

    def test_change_password_user_not_found(self):
        user_id = int(os.environ.get("TEST_USER_ID"))
        token = os.environ.get("TEST_TOKEN")

        res = self.client.put(f"{URL_FRAGMENT}/change-password/{user_id}", headers={"Authorization": f"Bearer {token}"},
                              json={ "old_password": "johndeux", "new_password": "johndoe" })

        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "User not found").dict()    
    
    def test_change_password_successful(self):
        user_id = int(os.environ.get("TEST_USER_ID"))
        token = os.environ.get("TEST_TOKEN")

        res = self.client.put(f"{URL_FRAGMENT}/change-password/{user_id}", headers={"Authorization": f"Bearer {token}"},
                              json={ "old_password": "johndoe", "new_password": "johndeux" })

        assert res.status_code == 200
        assert res.json() == Response[bool](data = True, code = 200, message = "User password changed succesfully").dict()
  
    def test_reset_password_user_not_found(self):
        res = self.client.post(f"{URL_FRAGMENT}/reset-password", json={ "email": "mary@poppins.com" })
        
        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "User not found").dict()
        
    def test_reset_password_successful(self):
        res = self.client.post(f"{URL_FRAGMENT}/reset-password", json={ "email": "johndoe@doe.com" })
        
        assert res.status_code == 200
        assert res.json() == Response[bool](data = True, code = 200, message="Password reset succesfully. New auto-generated password sent to email.").dict()
