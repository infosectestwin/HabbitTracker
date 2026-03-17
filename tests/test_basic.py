import unittest
import os
from app import create_app, db
from app.models import User, Habit
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # In-memory DB

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        u = User(username='testuser', email='test@example.com')
        u.set_password('cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_habit_creation(self):
        u = User(username='testuser', email='test@example.com')
        db.session.add(u)
        db.session.commit()
        
        h = Habit(name='Run', category='health', author=u)
        db.session.add(h)
        db.session.commit()
        
        self.assertEqual(h.author, u)
        self.assertEqual(u.habits.count(), 1)

if __name__ == '__main__':
    unittest.main()
