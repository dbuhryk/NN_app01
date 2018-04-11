# coding: utf-8
"""
Test suite for performance profiling and testing with isolated HTTP WEB Server in a standalone process
"""
from app01.app01_imp import app
from multiprocessing import Process
from time import sleep
import socket
import unittest
from urllib3 import HTTPConnectionPool
import os
import timeit
import logging
import json

app.config["TESTING"] = True
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def run_server(**kwargs):
    app.run(**kwargs)


class PerfTestCase(unittest.TestCase):
    """
    Tests multiple requests to a standalone HTTP server process
    """
    @classmethod
    def setUpClass(cls):
        cls.path = os.path.dirname(__file__)
        cls.resources_path = cls.path + "/resources/"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        cls.port = sock.getsockname()[1]
        sock.close()
        with app.app_context():
            cls.server = Process(target=run_server, kwargs={'host': 'localhost', 'port': cls.port})
            cls.server.start()
            sleep(5)

    def test_form_upload_sample_01(self):
        """
        Multiple Upload Form calls to isolated HTTP Server process
        """
        pool = HTTPConnectionPool('localhost', port=self.port, maxsize=1)

        def proc():
            response = pool.request('POST', '/', fields=dict(file=('file.txt', data),))
            self.assertEqual(response.status, 200)

        with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
            data = f.read()
            print(timeit.timeit(proc, number=100))

    def test_api_convert_sample_01(self):
        """
        Multiple API convert calls to isolated HTTP Server process
        """
        pool = HTTPConnectionPool('localhost', port=self.port, maxsize=1)

        def proc():
            response = pool.request(
                'POST',
                '/api/convert',
                headers={'Content-Type': 'application/json'},
                body=json.dumps({'text': data})
            )
            self.assertEqual(response.status, 200)

        with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
            data = f.read()
            print(timeit.timeit(proc, number=100))

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.join()


if __name__ == "__main__":
    unittest.main()
