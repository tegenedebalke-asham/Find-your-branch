from sqlalchemy import Column, Integer, String
from database import Base

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String)
    branch_name = Column(String)
    address = Column(String)
    phone = Column(String)
    city = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    atm_status = Column(String)
    working_hours = Column(String)
