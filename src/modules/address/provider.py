from .models import Address
from src.constants import ADDRESS_KEY
from typing import List, Union, Dict
from src.utils import randomInt
from src.response_models import Response
from .request_models import AddEditAddress as ReqAddress
from src.abstract_defs import IDatabase, IProvider

class AddressProvider(IProvider[Address]):
    db: IDatabase = None

    def __init__(self, db: IDatabase):
        self.db = db
    
    def getAll(self) -> Response[List[Address]]:
        data: Dict[str, dict] = self.db.get(ADDRESS_KEY) or {}
        addresses = [Address(**address) for address in data.values()]
        
        return Response[List[Address]](data = addresses, code = 200, message = "{0} Address(es) returned".format(len(addresses)))
    
    def get(self, id: int) -> Union[Response[Address], Response]:
        addresses: Dict[str, dict] = self.db.get(ADDRESS_KEY) or {}
        response: Union[Response[Address], Response] = None
        address: dict = addresses.get(str(id))
        
        if address:
            response = Response[Address](data = Address(**address), code = 200, message = "Address returned")
        else:
            response = Response(data = None, code = 404, message = "Address not found")

        return response
        
    def add(self, req: ReqAddress) -> Union[Response[Address], Response]:
        addresses: Dict[str, dict] = self.db.get(ADDRESS_KEY) or {}
        response: Union[Response[Address], Response] = None
        email_exists: bool = None

        for addr in addresses.values():
            if addr["email"] == req.email:
                email_exists = True
        else:
            if not email_exists:
                address = Address(name = req.name, email = req.email, id = randomInt())
                addresses[str(address.id)] = address.dict()

                self.db.set(ADDRESS_KEY, addresses)

                response = Response[Address](data = address, code = 201, message = "Address saved")
            else:
                response = Response(data = None, code = 400, message = "Email already in use by another address")
                
        return response

    def delete(self, id: int) -> Response:
        _id = str(id)
        addresses: Dict[str, dict] = self.db.get(ADDRESS_KEY) or {}
        response: Response = None
        
        if addresses.get(_id): 
            addresses.pop(_id)
            self.db.set(ADDRESS_KEY, addresses)

            response = Response(data = None, code = 200, message = "Address deleted")
        else:
            response = Response(data = None, code = 404, message = "Address not found")
        
        return response

    def edit(self, id: int, req: ReqAddress) -> Union[Response[Address], Response]:
        _id = str(id)
        addresses: Dict[str, dict] = self.db.get(ADDRESS_KEY) or {}
        response: Union[Response[Address], Response] = None
        email_exists: bool = False
        
        if addresses.get(_id):
            for addr in addresses.items():
                if addr[0] != _id and addr[1]["email"] == req.email:
                    email_exists = True
            else:
                if not email_exists:
                    addresses[_id]["name"] = req.name
                    addresses[_id]["email"] = req.email

                    self.db.set(ADDRESS_KEY, addresses)
                            
                    response = Response[Address](data = Address(**addresses.get(_id)), code = 200, message = "Address modified")
                else:
                    response = Response(data = None, code = 400, message = "Email already in use by another address")
        else:
            response = Response(data = None, code = 404, message = "Address not found")
            
        return response