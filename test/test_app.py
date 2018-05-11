import unittest
import json
from app import create_app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_get(self):
        response = self.client.get('/')
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['data']['status'], 'ok')

    def test_post(self):
        response = self.client.post(
            '/',
            data=json.dumps(dict(body='This sentences tis ha&rd to <> [] () pa~rse!')),
            content_type='application/json')
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['data']['rawSentence'],
                         'This sentences tis ha&rd to <> [] () pa~rse!')
        self.assertEqual(json_response['data']['cleanSentence'],
                        'This sentences tis ha rd to    parse')

        parsedSentence = [
            "This",
            "sentences",
            "tis",
            "hard",
            "to",
            "parse"
        ]
        self.assertEqual(json_response['data']['parsedSentence'], parsedSentence)
        self.assertEqual(json_response['data']['6gram'][0],parsedSentence)

        response = self.client.post('/', )
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['data']['error'],
                         'Unable to process request')

    def test_head(self):
        # HEAD Test - Returns status/ok, 200
        response = self.client.head('/')
        self.assertEqual(response.status_code, 200)

    def test_unusedmethods(self):
        response = self.client.put('/')
        self.assertEqual(response.status_code, 405)

        response = self.client.delete('/')
        self.assertEqual(response.status_code, 405)

        response = self.client.options('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.trace('/')
        self.assertEqual(response.status_code, 405)

    def test_404(self):
        response = self.client.get('/wrong/path')
        self.assertEqual(response.status_code, 404)
