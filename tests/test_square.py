import unittest
from app import app

class TestSquareAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_input(self):
        response = self.app.post('/square', json={'number': 4})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'number': 4, 'square': 16})

    def test_invalid_input(self):
        response = self.app.post('/square', json={'number': 'invalid'})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()