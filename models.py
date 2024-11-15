# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB  # 
from database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    file_metadata = Column(JSONB)  

