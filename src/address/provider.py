from src.address.models import Address
from src.constants import ADDRESS_KEY
from typing import List
from src.utils import randomInt
import src.db as db

def getAddresses():
    data: List[Address] = db.get(ADDRESS_KEY) or []
    return { "data": data, "code": 200, "message": "{0} Address(es) returned".format(len(data)) }

def getAddress(id: int):
    addresses: List[Address] = db.get(ADDRESS_KEY) or []
    address: Address = None
    
    for a in addresses:
        if a["id"] == id:
            address = a
    else:
        if address:
            return { "data": address, "code": 200, "message": "Address returned" }
        else:
            return { "data": None, "code": 404, "message": "Address not found" }
    
def addAddress(req: dict):
    addresses: List[Address] = db.get(ADDRESS_KEY) or []
    email_exists: bool = False
    
    for a in addresses:
        if a["email"] == req["email"]:
            email_exists = True
    else:
        if not email_exists:
            address = dict(Address(name = req["name"], email = req["email"], id = randomInt()))
            
            addresses.append(address)
            db.set(ADDRESS_KEY, addresses)

            return { "data": address, "code": 200, "message": "Address saved" }
        else:
            return { "data": None, "code": 400, "message": "Email already in use by another address" }

def deleteAddress(id: int):
    addresses: List[Address] = db.get(ADDRESS_KEY) or []
    address_index = None
    
    for i in range(len(addresses)):
        if addresses[i]["id"] == id:
            address_index = i
    else:
        if address_index: 
            del addresses[address_index]
            db.set(ADDRESS_KEY, addresses)

            return { "data": None, "code": 200, "message": "Address deleted" }
        else:
            return { "data": None, "code": 404, "message": "Address not found" }

def editAddress(id: int, req: dict):
    addresses: List[Address] = db.get(ADDRESS_KEY) or []
    address_index = None
    email_exists_index = None
    
    for i in range(len(addresses)):
        if addresses[i]["id"] == id:
            address_index = i

        if addresses[i]["email"] == req["email"]:
            email_exists_index = i
    else:
        if address_index:
            if not email_exists_index or (email_exists_index and email_exists_index == address_index):
                address = addresses[address_index]
                address["name"] = req["name"]
                address["email"] = req["email"]
                
                del addresses[address_index]

                addresses.insert(address_index, address)
                db.set(ADDRESS_KEY, addresses)
                        
                return { "data": address, "code": 200, "message": "Address modified" }
            else:
                return { "data": None, "code": 400, "message": "Email already in use by another address" }
        else:
            return { "data": None, "code": 404, "message": "Address not found" }