from src.modules.address.models import Address
from src.constants import ADDRESS_KEY
from typing import List, Union
from src.utils import randomInt
from src.response_models import Response
from src.modules.address.request_models import AddEditAddress as ReqAddress
from src.db import IDatabase
from src.abstract_defs import IProvider

class AddressProvider(IProvider[Address]):
    db: IDatabase = None

    def __init__(self, db: IDatabase):
        self.db = db
    
    def getAll(self) -> Response[List[Address]]:
        data: List[dict] = self.db.get(ADDRESS_KEY) or []
        
        return Response[List[Address]](data = data, code = 200, message = "{0} Address(es) returned".format(len(data)))
    
    def get(self, id: int) -> Union[Response[Address], Response]:
        addresses: List[dict] = self.db.get(ADDRESS_KEY) or []
        response: Union[Response[Address], Response] = None
        address: dict = None
        
        for addr in addresses:
            if addr["id"] == id:
                address = addr
        else:
            if address:
                response = Response[Address](data = Address(**address), code = 200, message = "Address returned")
            else:
                response = Response(data = None, code = 404, message = "Address not found")
        
        return response
        
    def add(self, req: ReqAddress) -> Union[Response[Address], Response]:
        addresses: List[dict] = self.db.get(ADDRESS_KEY) or []
        response: Union[Response[Address], Response] = None
        email_exists: bool = None

        for addr in addresses:
            if addr["email"] == req.email:
                email_exists = True
        else:
            if not email_exists:
                address = Address(name = req.name, email = req.email, id = randomInt())
                
                addresses.append(address.dict())
                self.db.set(ADDRESS_KEY, addresses)

                response = Response[Address](data = address, code = 201, message = "Address saved")
            else:
                response = Response(data = None, code = 400, message = "Email already in use by another address")
                
        return response

    def delete(self, id: int) -> Response:
        addresses: List[dict] = self.db.get(ADDRESS_KEY) or []
        response: Response = None
        address_index: int = None
        
        for i in range(len(addresses)):
            if addresses[i]["id"] == id:
                address_index = i
        else:
            if address_index is not None: 
                del addresses[address_index]
                self.db.set(ADDRESS_KEY, addresses)

                response = Response(data = None, code = 200, message = "Address deleted")
            else:
                response = Response(data = None, code = 404, message = "Address not found")
        
        return response

    def edit(self, id: int, req: ReqAddress) -> Union[Response[Address], Response]:
        addresses: List[dict] = self.db.get(ADDRESS_KEY) or []
        response: Union[Response[Address], Response] = None
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
                    self.db.set(ADDRESS_KEY, addresses)
                            
                    response = Response[Address](data = Address(**address), code = 200, message = "Address modified")
                else:
                    response = Response(data = None, code = 400, message = "Email already in use by another address")
            else:
                response = Response(data = None, code = 404, message = "Address not found")
            
        return response