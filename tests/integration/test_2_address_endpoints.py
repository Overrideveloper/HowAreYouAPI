from fastapi.testclient import TestClient
from src.server import app
from src.response_models import Response
import src.modules.address as AddressModule
import os
import logging

URL_FRAGMENT = "/api/address"

class Test2_AddressEndpoints:
    client = TestClient(app)
    
    def test_get_addresses_empty(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert len(res.json()["data"]) == 0
    
    def test_get_address_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(f"{URL_FRAGMENT}/2901", headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 404
        assert res.json() == Response(data = None, code = 404, message = "Address not found").dict()
        
    def test_create_address_missing_payload(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.post(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 400
        
    def test_create_address_successful(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.post(URL_FRAGMENT, json={ "name": "Mary Poppins", "email": "mary@poppins.com"}, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 201
        assert res.json()["data"]["name"] == "Mary Poppins"
        assert res.json()["data"]["email"] == "mary@poppins.com"
        
        os.environ["TEST_ADDRESS_ID"] = str(res.json()["data"]["id"])
    
    def test_create_address_email_in_use(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.post(URL_FRAGMENT, json={ "name": "Martha Mary Poppins", "email": "mary@poppins.com"}, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 400
        assert res.json() == Response(data = None, code = 400, message = "Email already in use by another address").dict()  
    
    def test_create_address_successful_1(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.post(URL_FRAGMENT, json={ "name": "Martha Mary Poppins", "email": "martha@poppins.com"}, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 201
        assert res.json()["data"]["name"] == "Martha Mary Poppins"
        assert res.json()["data"]["email"] == "martha@poppins.com"

    def test_get_addresses(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.get(URL_FRAGMENT, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert len(res.json()["data"]) == 2
        
    def test_get_address(self):
        token = os.environ.get("TEST_TOKEN")
        address_id = int(os.environ.get("TEST_ADDRESS_ID"))

        res = self.client.get(f"{URL_FRAGMENT}/{address_id}", headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 200
        assert res.json()["data"]
        assert res.json()["data"]["id"] == address_id
        
    def test_edit_address_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.put(f"{URL_FRAGMENT}/2091", json={ "name": "Mary Popular", "email": "mary@popculture.com"}, headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code
        assert res.json() == Response(data = None, code = 404, message = "Address not found").dict()
    
    def test_edit_address_email_in_use(self):
        token = os.environ.get("TEST_TOKEN")
        address_id = int(os.environ.get("TEST_ADDRESS_ID"))
        res = self.client.put(f"{URL_FRAGMENT}/{address_id}", json={ "name": "Mary Martha Poppins", "email": "martha@poppins.com"}, headers={"Authorization": f"Bearer {token}"})

        assert res.status_code == 400
        assert res.json() == Response(data = None, code = 400, message = "Email already in use by another address").dict()  
    
    def test_edit_address_successful(self):
        token = os.environ.get("TEST_TOKEN")
        address_id = int(os.environ.get("TEST_ADDRESS_ID"))
        address = AddressModule.models.Address(id = address_id, name = "Mary Popular", email = "mary@popculture.com")

        res = self.client.put(f"{URL_FRAGMENT}/{address_id}", json={ "name": address.name, "email": address.email }, headers={"Authorization": f"Bearer {token}"})
        
        
        assert res.status_code
        assert res.json() == Response(data = address, code = 200, message = "Address modified").dict()
        
    def test_delete_not_found(self):
        token = os.environ.get("TEST_TOKEN")
        res = self.client.delete(f"{URL_FRAGMENT}/2091", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code
        assert res.json() == Response(data = None, code = 404, message = "Address not found").dict()
                
    def test_delete_successful(self):
        token = os.environ.get("TEST_TOKEN")
        address_id = int(os.environ.get("TEST_ADDRESS_ID"))
        res = self.client.delete(f"{URL_FRAGMENT}/{address_id}", headers={"Authorization": f"Bearer {token}"})
        
        assert res.status_code
        assert res.json() == Response(data = None, code = 200, message = "Address deleted").dict()
