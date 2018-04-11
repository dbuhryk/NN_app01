# coding: utf-8
"""
Test suite for testing Application View
"""
import unittest
import logging
import io
import os
from app01.app01_imp import app


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

app.config["TESTING"] = True


class FlaskrWebTestCase(unittest.TestCase):
    """
    Tests basic View functionality
    """
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.path = os.path.dirname(__file__)
        cls.resources_path = cls.path + "/resources/"

    def test_get_root_01(self):
        """
        Basic check if root index page is available
        """
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_01(self):
        """
        Basic check nonexistent endpoint
        """
        with app.test_client() as client:
            response = client.get('/api')
            self.assertEqual(response.status_code, 404)

    def test_form_upload_empty_01(self):
        """
        Upload clicked with empty file name
        """
        with app.test_client() as client:
            response = client.post('/', data=dict(file=(io.BytesIO(b'some_content'), ''),))
            self.assertEqual(response.status_code, 302)
            response = client.post('/', data=dict(file=(io.BytesIO(b'some_content'), ''),), follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_form_upload_toolarge_01(self):
        """
        Upload clicked with large file
        """
        with app.test_client() as client:
            b = io.BytesIO(b' ' * (app.config['MAX_CONTENT_LENGTH'] + 1024))
            b.seek(0)
            response = client.post('/', data=dict(file=(b, 'large_file.txt'),))
            self.assertEqual(response.status_code, 413)

    def test_form_upload_samplefile_01(self):
        """
        Upload clicked with sample file
        """
        with app.test_client() as client:
            with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                response = client.post('/', data=dict(
                    file=(io.BytesIO(data.encode('utf-8')), 'file.txt'),
                ))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(u'Oracle®' in response.data.decode('utf-8'))

    def test_form_upload_exception_01(self):
        """
        Simulating Model exception after Upload is clicked
        """
        def mockup_proc(*args, **kwargs):
            raise RuntimeError
        with app.test_client() as client:
            from app01.app01_imp import get_model
            old_model_proc = get_model().replace
            get_model().replace = mockup_proc
            response = client.post('/', data=dict(file=(io.BytesIO(b'some_content'), 'file.txt'),))
            get_model().replace = old_model_proc
            self.assertEqual(response.status_code, 302)

    def test_form_upload_counter_01(self):
        """
        Verification for incremental call counter
        """
        def parse_counter_value(s):
            _data = s.data.decode('utf-8')
            pos_start = _data.find('<h6>Application call counter: ') + len('<h6>Application call counter: ')
            pos_end = _data.find('</h6>', pos_start)
            return int(_data[pos_start:pos_end])

        with app.test_client() as client:
            response = client.get('/')
            counter_before = parse_counter_value(response)
            self.test_form_upload_samplefile_01()
            response = client.get('/')
            counter_after = parse_counter_value(response)
            self.assertEqual(counter_before + 1, counter_after)


if __name__ == "__main__":
    unittest.main()
