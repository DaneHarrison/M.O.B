import numpy as np
import psycopg2
import cv2
import sys

sys.path.append('../../src/logic/trainingServer')
from training import Trainer



path = '../../res/trainingData/'
model = Trainer(height = 80, width = 70, num_images=320, img_path=path)
model.run_training()
model.test_model(debug=True, stats=True, testpath='../../res/testingData/')

print("#========================")
print("Above answer if from the trainer")
print("Below answer if from the trainer")
print("#========================")




testing_path = '../../res/testingData/49_5.jpg'
img = cv2.imread(testing_path, 0)
img_col = np.array(img, dtype='float64').flatten()
img_col -= model.mean_vector 
img_col = np.reshape(img_col, (70*80, 1))  
S = model.eVectors * img_col 

S = S.reshape((1,len(S)))
S = str(S.tolist())[1:-1]

con = psycopg2.connect(
    host='localhost',
    port=5432,
    database='MOB',
    user='user',
    password='password'
)

cur = con.cursor()
cur.execute(f"SELECT find_min(ARRAY{S})")

yo = cur.fetchall()
print(yo)
cur.close()
con.close()
print('#-------------------------------------------')

con = psycopg2.connect(
    host='localhost',
    port=5433,
    database='MOB',
    user='user',
    password='password'
    )

cur = con.cursor()
cur.execute(f"SELECT find_min(ARRAY{S})")

yo = cur.fetchall()
print(yo)
cur.close()
con.close()
print('#-------------------------------------------')
con = psycopg2.connect(
        host='localhost',
        port=5434,
        database='MOB',
        user='user',
        password='password'
)
cur = con.cursor()
cur.execute(f"SELECT find_min(ARRAY{S})")

yo = cur.fetchall()
print(yo)
cur.close()
con.close()