# coding: utf-8
from app01.app01_imp import app
from multiprocessing import Process
from time import sleep
import socket
import unittest
from urllib3 import HTTPConnectionPool
import os
import timeit
import logging

app.config["TESTING"] = True
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def run_server(**kwargs):
    app.run(**kwargs)


class PerfTestCase(unittest.TestCase):
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
        pool = HTTPConnectionPool('localhost', port=self.port, maxsize=1)
        def proc():
            response = pool.request('POST', '/', fields=dict(file=('file.txt', data),))
            self.assertEqual(response.status, 200)

        with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
            data = f.read()
            print(timeit.timeit(proc, number=1000))

    def tearDown(self):
        self.server.terminate()
        self.server.join()


if __name__ == "__main__":
    unittest.main()
