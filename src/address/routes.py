from fastapi import APIRouter, Path, Body
from fastapi.responses import JSONResponse
from src.response_models import Response
from src.address.request_models import AddEditAddress as ReqAddress
from src.address.models import Address
from typing import List, Union
import src.address.provider as provider
from src.utils import generate404ResContent, generate400ResContent

address = APIRouter()

@address.get('/', summary="Get Addresses", description="Get a list of all addresses", response_model=Response[List[Address]])
def getAddresses():
    data: Response[List[Address]] = provider.getAddresses()

    return JSONResponse(content = data.dict(), status_code = data.code)

@address.get('/{id}', summary="Get Address", description="Get an address", response_model=Response[Address],
responses={ 404: generate404ResContent("Address"), 400: generate400ResContent(), 422: {} })
def getAddress(id: int = Path(..., gt=0, description="The ID of the address to get")):
    data: Union[Response[Address], Response] = provider.getAddress(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@address.post('/', summary="Add Address", description="Create and save an address", response_model=Response[Address],
responses={ 400: generate400ResContent(), 422: {} })
def addAddress(payload: ReqAddress = Body(..., description="The address to create")):
    data: Union[Response[Address], Response] = provider.addAddress(payload)

    return JSONResponse(content = data.dict(), status_code = data.code)

@address.delete('/{id}', summary="Delete Address", description="Delete an address", response_model=Response,
responses={ 400: generate400ResContent(), 404: generate404ResContent("Address"), 422: {} })
def deleteAddress(id: int = Path(..., gt=0, description="The ID of the address to delete")):
    data: Response = provider.deleteAddress(id)

    return JSONResponse(content = data.dict(), status_code = data.code)

@address.put('/{id}', summary="Edit Address", description="Edit an address", response_model=Response[Address],
responses={ 400: generate400ResContent(), 404: generate404ResContent("Address"), 422: {} })
def editAddress(id: int = Path(..., gt=0, description="The ID of the address to edit"), payload: ReqAddress = Body(..., description="The address data to be used in the edit")):
    data: Union[Response[Address], Response] = provider.editAddress(id, payload)

    return JSONResponse(content = data.dict(), status_code = data.code)