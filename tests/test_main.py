import io
import unittest

from parameterized import parameterized

from src import main


class MainTestCase(unittest.TestCase):
    @parameterized.expand([
        ('/', 200),
        ('/stock', 200),
        ('/intraday', 200),
        ('/evaluation', 200),
        ('/forward', 200),
        ('/stock/intraday/ticker', 200),
        ('/process', 200),
        ('/process/start/process_name', 200),
        ('/process/stop/process_name', 200),
        ('/import', 200),
        ('/export', 200),
        ('/export/intraday', 200),
        ('/invalid', 404),
    ])
    def test_get(self, path, code):
        main.app.testing = True
        client = main.app.test_client()
        response = client.get(path, environ_base={'REMOTE_ADDR': '127.0.0.1'})
        self.assertEqual(response.status_code, code)

    def test_post(self):
        main.app.testing = True
        client = main.app.test_client()
        data = {'file': (io.BytesIO(b'{}'), 'intraday.json')}
        response = client.post('/import/intraday', environ_base={'REMOTE_ADDR': '127.0.0.1'}, data=data,
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
