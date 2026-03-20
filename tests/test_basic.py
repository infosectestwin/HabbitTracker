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
        self.client = self.app.test_client()

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

    def test_security_headers_present(self):
        """Test that security headers are present on the main route."""
        response = self.client.get('/')
        
        # Check that all security headers are present
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertIn('X-Frame-Options', response.headers)
        self.assertIn('Referrer-Policy', response.headers)
        
        # Check specific header values
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')
        self.assertEqual(response.headers['Referrer-Policy'], 'strict-origin-when-cross-origin')
        
        # Check CSP contains expected directives (should include nonce)
        csp = response.headers['Content-Security-Policy']
        self.assertIn("default-src 'self'", csp)
        self.assertIn("script-src 'self' 'nonce-", csp)  # Should contain nonce
        self.assertIn("style-src 'self' 'nonce-", csp)   # Should contain nonce
        self.assertNotIn("'unsafe-inline'", csp)         # Should not allow unsafe-inline

    def test_hsts_header_on_https(self):
        """Test that HSTS header is set when request is over HTTPS."""
        # Simulate HTTPS request by overriding the request context
        with self.app.test_request_context('/', environ_overrides={'wsgi.url_scheme': 'https'}):
            response = self.client.get('/', environ_overrides={'wsgi.url_scheme': 'https'})
            self.assertIn('Strict-Transport-Security', response.headers)
            self.assertEqual(response.headers['Strict-Transport-Security'], 'max-age=31536000; includeSubDomains')

    def test_hsts_header_not_on_http(self):
        """Test that HSTS header is NOT set on HTTP requests."""
        response = self.client.get('/')
        self.assertNotIn('Strict-Transport-Security', response.headers)

if __name__ == '__main__':
    unittest.main()
