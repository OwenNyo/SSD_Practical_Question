import unittest
from app import app, COMMON_PASSWORDS

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page_loads(self):
        """Check if home page loads with 200 status and contains form elements."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<form method="POST">', response.data)
        self.assertIn(b'name="password"', response.data)

    def test_common_password_rejected(self):
        """Submit a weak/common password and expect an error message."""
        # Pick one known weak password from your common_passwords.txt
        weak_password = next(iter(COMMON_PASSWORDS))
        response = self.client.post('/', data={'password': weak_password})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid password.', response.data)

    def test_strong_password_redirects(self):
        """Submit a strong password and expect a redirect to /welcome."""
        strong_password = 'S3cure!Pass123'
        response = self.client.post('/', data={'password': strong_password}, follow_redirects=False)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/welcome', response.headers['Location'])

    def test_welcome_page_receives_password(self):
        """Check if welcome page loads with a password query string."""
        response = self.client.get('/welcome?password=S3cure!Pass123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'S3cure!Pass123', response.data)

    def test_logout_redirects_to_home(self):
        """Check if /logout route redirects back to /."""
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()
