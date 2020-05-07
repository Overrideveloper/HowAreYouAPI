from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.address.request_models import AddEditAddress as ReqAddress
import src.address.provider as provider

address = APIRouter()

@address.get('/')
def getAddresses():
    data: Response = provider.getAddresses()

    return JSONResponse(content = dict(data), status_code = data.code)

@address.get('/{id}')
def getAddress(id: int):
    data: Response = provider.getAddress(id)

    return JSONResponse(content = dict(data), status_code = data.code)

@address.post('/')
def addAddress(payload: ReqAddress):
    data: Response = provider.addAddress(payload)

    return JSONResponse(content = dict(data), status_code = data.code)

@address.delete('/{id}')
def deleteAddress(id: int):
    data: Response = provider.deleteAddress(id)

    return JSONResponse(content = dict(data), status_code = data.code)

@address.put('/{id}')
def editAddress(id: int, payload: ReqAddress):
    data: Response = provider.editAddress(id, payload)

    return JSONResponse(content = dict(data), status_code = data.code)