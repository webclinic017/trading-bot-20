import unittest

from src import app


class MainTest(unittest.TestCase):

    def test_index(self):
        app.testing = True
        client = app.test_client()
        response = client.get('/', environ_base={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response.data.decode('utf-8'), '127.0')
