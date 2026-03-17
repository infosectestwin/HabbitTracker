import unittest
from app.blueprints.auth import is_password_strong

class TestPasswordValidation(unittest.TestCase):
    def test_too_short(self):
        is_strong, msg = is_password_strong("Sh1@abc")
        self.assertFalse(is_strong)
        self.assertEqual(msg, "Password must be at least 8 characters long.")

    def test_no_lowercase(self):
        is_strong, msg = is_password_strong("STRONG1@")
        self.assertFalse(is_strong)
        self.assertEqual(msg, "Password must contain at least one lowercase letter.")

    def test_no_uppercase(self):
        is_strong, msg = is_password_strong("strong1@")
        self.assertFalse(is_strong)
        self.assertEqual(msg, "Password must contain at least one uppercase letter.")

    def test_no_number(self):
        is_strong, msg = is_password_strong("Strong@@")
        self.assertFalse(is_strong)
        self.assertEqual(msg, "Password must contain at least one number.")

    def test_no_special_char(self):
        is_strong, msg = is_password_strong("Strong123")
        self.assertFalse(is_strong)
        self.assertEqual(msg, "Password must contain at least one special character.")

    def test_valid_password(self):
        is_strong, msg = is_password_strong("Strong@123")
        self.assertTrue(is_strong)
        self.assertEqual(msg, "")

if __name__ == '__main__':
    unittest.main()
