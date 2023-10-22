import sys
import os
import re
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)
from sqlalchemy.orm import validates
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from datetime import datetime

from core.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    verified_at = Column(DateTime, nullable=True, default=None)
    registered_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    @validates('email')
    def validate_email(self, key, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(email_pattern, email) is None:
            raise ValueError("Invalid email address")
        return email