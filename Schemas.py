from pydantic import BaseModel

class BranchBase(BaseModel):
    bank_name: str
    branch_name: str
    address: str
    phone: str
    city: str
    latitude: str
    longitude: str
    atm_status: str
    working_hours: str

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: int

    class Config:
        orm_mode = True
