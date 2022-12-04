import cv2, base64, json, requests

photo = cv2.imread('../../res/testingData/9_1.jpg', 0)
photo_in_base64 = base64.b64encode(photo)
photo_as_string = photo_in_base64.decode('utf-8')
photo_as_json = json.dumps({"Photo": photo_as_string}, indent=2)

res = requests.post('http://192.168.49.2:80/', json = photo_as_json)
res = json.loads(res.json())
print(res)