from tests.unit.mocks.db_mock import DatabaseMock
from src.modules.address.provider import AddressProvider
from src.response_models import Response
from src.modules.address.models import Address
from typing import List
from src.db import IDatabase
from src.constants import ADDRESS_KEY
from src.modules.address.request_models import AddEditAddress
from copy import deepcopy

class TestAddressProvider:
    dbMock: IDatabase = DatabaseMock()
    addressProvider: AddressProvider = AddressProvider(dbMock)
    address_list: List[dict] = list([
        Address(id = 1, name = "John Doe", email = "john@doe.com").dict(),
        Address(id = 2, name = "Mary Poppins", email = "mary@poppins.com").dict()
    ])
    
    def test_creation(self):
        assert self.addressProvider is not None
    
    def test_get_all_empty(self):
        res = self.addressProvider.getAll()
        
        assert isinstance(res, Response[List[Address]])
        assert res.code == 200
        assert len(res.data) == 0
        
    def test_get_all_non_empty(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))

        res = self.addressProvider.getAll()
        
        assert isinstance(res, Response[List[Address]])
        assert res.code == 200
        assert len(res.data) == 2
        
        self.dbMock.remove(ADDRESS_KEY)
        
    def test_get_200(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))

        res = self.addressProvider.get(1)
        
        assert isinstance(res, Response[Address])
        assert res.code == 200
        assert isinstance(res.data, Address)
        assert res.data.dict() == self.address_list[0]
        
        self.dbMock.remove(ADDRESS_KEY)
        
    def test_get_404(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))

        res = self.addressProvider.get(99)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ADDRESS_KEY)
            
    def test_add_400(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))

        payload = AddEditAddress(name = "Doe Johnson", email = "john@doe.com")
        
        res = self.addressProvider.add(payload)
        
        assert isinstance(res, Response)
        assert res.code == 400
        assert not res.data
        
        self.dbMock.remove(ADDRESS_KEY)
    
    def test_add_201(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))

        payload = AddEditAddress(name = "Bilbo Baggins", email = "bilbo@lotr.com")
        
        res = self.addressProvider.add(payload)
        
        assert isinstance(res, Response[Address])
        assert res.code == 201
        assert isinstance(res.data, Address)
        assert res.data == Address(id = res.data.id, **payload.dict()).dict()
        
        self.dbMock.remove(ADDRESS_KEY)

    def test_delete_404(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))
        
        res = self.addressProvider.delete(99)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ADDRESS_KEY)
    
    def test_delete_200(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))

        res = self.addressProvider.delete(1)
        res1 = self.addressProvider.getAll()
        
        assert isinstance(res, Response)
        assert res.code == 200

        assert res1.code == 200
        assert len(res1.data) == 1
        assert res1.data[0] == self.address_list[1]

        self.dbMock.remove(ADDRESS_KEY)

    def test_edit_404(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))
        
        payload = AddEditAddress(name = "Bilbo Baggins", email = "bilbo@lotr.com")
        
        res = self.addressProvider.edit(99, payload)
        
        assert isinstance(res, Response)
        assert res.code == 404
        assert not res.data
        
        self.dbMock.remove(ADDRESS_KEY)
    
    def test_edit_400(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))
        
        payload = AddEditAddress(name = "Doe Johnson", email = "john@doe.com")
        
        res = self.addressProvider.edit(2, payload)
        
        assert isinstance(res, Response)
        assert res.code == 400
        assert not res.data
        
    def test_edit_200(self):
        self.dbMock.set(ADDRESS_KEY, deepcopy(self.address_list))
        
        payload = AddEditAddress(name = "Bilbo Baggins", email = "bilbo@lotr.com")
        
        res = self.addressProvider.edit(1, payload)
        res1 = self.addressProvider.getAll()
        
        assert isinstance(res, Response)
        assert res.code == 200
        assert res.data == Address(id = 1, **payload.dict()).dict()

        assert res1.code == 200
        assert len(res1.data) == len(self.address_list)
        assert res1.data[0] == res.data
        
    