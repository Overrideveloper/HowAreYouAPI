from fastapi import APIRouter, Response as HttpResponse
from src.response_models import Response
from src.address.request_models import AddEditAddress as Address
import src.address.provider as provider

address = APIRouter()

@address.get('/', response_model = Response, status_code = 200)
def getAddresses():
    return provider.getAddresses()

@address.get('/{id}', response_model = Response, status_code = 200)
def getAddress(id: int, response: HttpResponse):
    data: Response = provider.getAddress(id)
    response.status_code = data["code"]
    return data

@address.post('/', response_model = Response, status_code = 201)
def addAddress(payload: Address, response: HttpResponse):
    data: Response = provider.addAddress(dict(payload))
    response.status_code = data["code"]
    return data

@address.delete('/{id}', response_model = Response, status_code = 200)
def deleteAddress(id: int, response: HttpResponse):
    data: Response = provider.deleteAddress(id)
    response.status_code = data["code"]
    return data

@address.put('/{id}', response_model = Response, status_code = 200)
def editAddress(id: int, payload: Address, response: HttpResponse):
    data: Response = provider.editAddress(id, dict(payload))
    response.status_code = data["code"]
    return data