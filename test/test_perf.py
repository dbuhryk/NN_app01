# coding: utf-8
from app01.app01_imp import app
from multiprocessing import Process
from time import sleep
import socket
import unittest
import requests
import os
import timeit
import logging
# import cProfile
# import pstats
# from threading import Thread

app.config["TESTING"] = True
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

def run_server(**kwargs):
    # pr = cProfile.Profile()
    # pr.enable()
    app.run(**kwargs)
    # pr.disable()
    # s = io.StringIO()
    # ps = pstats.Stats(pr, stream=s)
    # ps.print_stats()
    # print(s.getvalue())


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

    @unittest.skip("Not implemented yet")
    def test_post_sample_01(self):
        def proc():
            response = requests.post('http://localhost:%s' % self.port, allow_redirects=False, files=dict(file=('file.txt', data),))
            self.assertEqual(response.status_code, 200)

        with open(self.resources_path + 'oracle.txt', 'r', encoding='utf-8') as f:
            data = f.read()
            timeit.timeit(proc, number=1)

    def tearDown(self):
        self.server.terminate()
        self.server.join()


if __name__ == "__main__":
    unittest.main()
