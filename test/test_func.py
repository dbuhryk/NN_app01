# coding: utf-8
from app01.app01_imp import app
from multiprocessing import Process
from time import sleep
import socket
import unittest
import requests
import os
import logging

app.config["TESTING"] = True
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def run_server(**kwargs):
    app.run(**kwargs)


class FlaskrFuncTestCase(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(__file__)
        self.resources_path = self.path + "/resources/"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        self.port = sock.getsockname()[1]
        sock.close()
        with app.app_context():
            self.server = Process(target=run_server, kwargs={'host': 'localhost', 'port': self.port})
            self.server.start()
            sleep(5)

    def test_post_sample_01(self):
        with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
            data = f.read()
            response = requests.post(
                'http://localhost:%s' % self.port,
                allow_redirects=False,
                files=dict(file=('file.txt', data),)
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u'Oracle®' in response.content.decode('utf-8'))

    def tearDown(self):
        self.server.terminate()
        self.server.join()


if __name__ == "__main__":
    unittest.main()
