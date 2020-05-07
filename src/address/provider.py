from src.address.models import Address
from src.constants import ADDRESS_KEY
from typing import List
from src.utils import randomInt
from src.response_models import Response
from src.address.request_models import AddEditAddress as ReqAddress
import src.db as db

def getAddresses() -> Response:
    data: List[dict] = db.get(ADDRESS_KEY) or []
    
    return Response(data = data, code = 200, message = "{0} Address(es) returned".format(len(data)))

def getAddress(id: int) -> Response:
    addresses: List[dict] = db.get(ADDRESS_KEY) or []
    response: Response = None
    address: dict = None
    
    for addr in addresses:
        if addr["id"] == id:
            address = addr
    else:
        if address:
            response = Response(data = address, code = 200, message = "Address returned")
        else:
            response = Response(data = None, code = 404, message = "Address not found")
    
    return response
    
def addAddress(req: ReqAddress) -> Response:
    addresses: List[dict] = db.get(ADDRESS_KEY) or []
    response: Response = None
    email_exists: bool = None

    for addr in addresses:
        if addr["email"] == req.email:
            email_exists = True
    else:
        if not email_exists:
            address = Address(name = req.name, email = req.email, id = randomInt())
            
            addresses.append(dict(address))
            db.set(ADDRESS_KEY, addresses)

            response = Response(data = dict(address), code = 201, message = "Address saved")
        else:
            response = Response(data = None, code = 400, message = "Email already in use by another address")
            
    return response

def deleteAddress(id: int) -> Response:
    addresses: List[dict] = db.get(ADDRESS_KEY) or []
    response: Response = None
    address_index: int = None
    
    for i in range(len(addresses)):
        if addresses[i]["id"] == id:
            address_index = i
    else:
        if address_index is not None: 
            del addresses[address_index]
            db.set(ADDRESS_KEY, addresses)

            response = Response(data = None, code = 200, message = "Address deleted")
        else:
            response = Response(data = None, code = 404, message = "Address not found")
    
    return response

def editAddress(id: int, req: ReqAddress) -> Response:
    addresses: List[dict] = db.get(ADDRESS_KEY) or []
    response: Response = None
    address_index: int = None
    email_exists_index: int = None
    
    for i in range(len(addresses)):
        if addresses[i]["id"] == id:
            address_index = i

        if addresses[i]["email"] == req.email:
            email_exists_index = i
    else:
        if address_index is not None:
            if email_exists_index is None or (email_exists_index is not None and email_exists_index == address_index):
                address = addresses[address_index]
                address["name"] = req.name
                address["email"] = req.email
                
                del addresses[address_index]

                addresses.insert(address_index, address)
                db.set(ADDRESS_KEY, addresses)
                        
                response = Response(data = address, code = 200, message = "Address modified")
            else:
                response = Response(data = None, code = 400, message = "Email already in use by another address")
        else:
            response = Response(data = None, code = 404, message = "Address not found")
        
    return response