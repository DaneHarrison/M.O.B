import unittest, sys, requests

sys.path.append('../../src/persistance')

from dbAdapter import DBAdapter

class Worker(unittest.TestCase):
    def test_worker_api(self):
        # load image
        # send as JSON to worker
        # wait for a response
        # assert response
        print()


if __name__ == '__main__':
    import nose2
    nose2.main()  