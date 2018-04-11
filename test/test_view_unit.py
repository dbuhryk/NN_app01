# coding: utf-8
import unittest
import logging
import io
import os
from app01.app01_imp import app


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

app.config["TESTING"] = True


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.path = os.path.dirname(__file__)
        self.resources_path = self.path + "/resources/"

    def test_get_root_01(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_get_other_01(self):
        with app.test_client() as client:
            response = client.get('/api')
            self.assertEqual(response.status_code, 404)

    def test_post_empty_01(self):
        with app.test_client() as client:
            response = client.post('/', data=dict(file=(io.BytesIO(b'some_content'), ''),))
            self.assertEqual(response.status_code, 302)
            response = client.post('/', data=dict(file=(io.BytesIO(b'some_content'), ''),), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_post_samplefile_01(self):
        with app.test_client() as client:
            with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                response = client.post('/', data=dict(
                    file=(io.BytesIO(data.encode('utf-8')), 'file.txt'),
                ))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(u'Oracle®' in response.data.decode('utf-8'))

    def test_post_exception_01(self):
        def mockup_proc(*args, **kwargs):
            raise RuntimeError
        with app.test_client() as client:
            from app01.app01_imp import get_model
            old_model_proc = get_model().replace
            get_model().replace = mockup_proc
            response = client.post('/', data=dict(file=(io.BytesIO(b'some_content'), 'file.txt'),))
            self.assertEqual(response.status_code, 302)
            get_model().replace = old_model_proc

    def test_test_counter_01(self):
        def parse_counter_value(s):
            _data = s.data.decode('utf-8')
            pos_start = _data.find('<h6>Application call counter: ') + len('<h6>Application call counter: ')
            pos_end = _data.find('</h6>', pos_start)
            return int(_data[pos_start:pos_end])

        with app.test_client() as client:
            response = client.get('/')
            counter_before = parse_counter_value(response)
            self.test_post_samplefile_01()
            response = client.get('/')
            counter_after = parse_counter_value(response)
            self.assertEqual(counter_before + 1, counter_after)


if __name__ == "__main__":
    unittest.main()
