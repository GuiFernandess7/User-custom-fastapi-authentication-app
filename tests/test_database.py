import unittest
import sys
import os
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.users.models import UserModel
from src.core.database import Base
from dotenv import load_dotenv
from src.core.config import get_settings
load_dotenv()
import os

settings = get_settings()

class TestUserModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self) -> None:
        self.session.rollback()
        self.session.query(UserModel).delete()
        self.session.commit()

    def test_user_creation(self):
        user = UserModel(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="hashed_password",
            is_active=False,
            is_verified=False
        )
        self.session.add(user)
        self.session.commit()

        retrieved_user = self.session.query(UserModel).filter_by(first_name="Test").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.last_name, "User")
        self.assertEqual(retrieved_user.email, "test@example.com")
        self.assertEqual(retrieved_user.password, "hashed_password")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            user = UserModel(
                first_name="Test",
                last_name="User",
                email="invalid_email",
                password="hashed_password",
                is_active=False,
                is_verified=False
            )
            self.session.add(user)
            self.session.commit()

if __name__ == "__main__":
    unittest.main()
