# coding: utf-8
"""
Test suite for testing Application RESTFULL API
"""
import unittest
import logging
import json
import os
import io
from app01.app01_imp import app


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

app.config["TESTING"] = True


class FlaskrApiTestCase(unittest.TestCase):
    """
    Tests basic RESTFULL API functionality
    """

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.path = os.path.dirname(__file__)
        cls.resources_path = cls.path + "/resources/"

    def test_get_callcounter_01(self):
        """
        Call counter is returned and of integer type
        """
        with app.test_client() as client:
            response = client.get('/api/callcounter')
            self.assertEqual(response.status_code, 200)
            res = json.loads(response.data.decode('utf8'))
            self.assertGreaterEqual(res['callcounter'], 0)

    def test_get_callcounter_exception_01(self):
        """
        Exception during callcounter calls
        """
        def mockup_proc(*args, **kwargs):
            raise RuntimeError
        with app.test_client() as client:
            from app01.app01_imp import get_model
            old_model_proc = get_model().call_counter
            get_model().call_counter = mockup_proc
            response = client.get('/api/callcounter')
            get_model().call_counter = old_model_proc
            self.assertEqual(response.status_code, 400)
            self.assertTrue(json.loads(response.data)['error'] is not None)

    def test_post_callcounter_01(self):
        """
        wrong HTTP method POST to callcounter endpoint
        """
        with app.test_client() as client:
            response = client.post('/api/callcounter')
            self.assertEqual(response.status_code, 405)

    def test_post_rawconvert_sample_01(self):
        """
        RAW convert endpoint with sample file
        """
        with app.test_client() as client:
            with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                response = client.post('/raw/convert', data=io.BytesIO(data.encode('utf-8')))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(u'Oracle®' in response.data.decode('utf-8'))

    def test_post_rawconvert_toolarge_01(self):
        """
        RAW convert endpoint with too large file
        """
        with app.test_client() as client:
            b = io.BytesIO(b' ' * (app.config['MAX_CONTENT_LENGTH'] + 1024))
            b.seek(0)
            response = client.post('/raw/convert', data=b)
            self.assertEqual(response.status_code, 413)

    def test_post_rawconvert_exception_01(self):
        """
        Exception during a raw convert endpoint invocation
        """
        def mockup_proc(*args, **kwargs):
            raise RuntimeError
        with app.test_client() as client:
            from app01.app01_imp import get_model
            old_model_proc = get_model().replace
            get_model().replace = mockup_proc
            response = client.post('/raw/convert', data=io.BytesIO(b''))
            get_model().replace = old_model_proc
            self.assertEqual(response.status_code, 400)

    def test_post_apiconvert_sample_01(self):
        """
        API convert endpoint with sample file
        """
        with app.test_client() as client:
            with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                response = client.post('/api/convert', content_type='application/json', data=json.dumps({'text': data}))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(u'Oracle®' in json.loads(response.data)['text'])

    def test_post_apiconvert_brokenjson_01(self):
        """
        API convert with broken JSON
        """
        with app.test_client() as client:
            with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                response = client.post('/api/convert', content_type='application/json', data=json.dumps({'': data}))
            self.assertEqual(response.status_code, 400)
            self.assertTrue(json.loads(response.data)['error'] is not None)

    def test_post_apiconvert_exception_01(self):
        """
        Exception during a API convert endpoint invocation
        """
        def mockup_proc(*args, **kwargs):
            raise RuntimeError
        with app.test_client() as client:
            from app01.app01_imp import get_model
            old_model_proc = get_model().replace
            get_model().replace = mockup_proc

            with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                response = client.post('/api/convert', content_type='application/json', data=json.dumps({'': data}))

            get_model().replace = old_model_proc
            self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
