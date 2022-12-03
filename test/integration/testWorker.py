import unittest, requests, sys, requests, nose2, json, base64, cv2, numpy

sys.path.append('../../src/persistance')

from dbAdapter import DBAdapter

class Worker(unittest.TestCase):
    def test_worker_api(self):
        photo = cv2.imread('../../res/testingData/9_1.jpg', 0)
        photo_in_base64 = base64.b64encode(photo)
        photo_as_string = photo_in_base64.decode('utf-8')
        photo_as_json = json.dumps({"Photo": photo_as_string}, indent=2)

        res = requests.post('http://localhost:4000/', json = photo_as_json)
        res = json.loads(res.json())
        self.assertEqual(res["Name"], 'Milo Wolfe')


if __name__ == '__main__':
    nose2.main()  