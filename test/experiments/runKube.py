photo = cv2.imread('../../res/testingData/9_1.jpg', 0)
photo_in_base64 = base64.b64encode(photo)
photo_as_string = photo_in_base64.decode('utf-8')
photo_as_json = json.dumps({"Photo": photo_as_string}, indent=2)

res = requests.post('http://localhost:80/', json = photo_as_json)
res = json.loads(res.json())
print(res)