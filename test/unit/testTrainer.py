import sys

sys.path.append('../../src/logic/trainingServer')
from training import Trainer

path = '../../res/trainingData/'
model = Trainer(height = 80, width = 70, num_images=320, img_path=path)
model.run_training()
model.test_model(debug=True, stats=True, testpath='../../res/testingData/')
print()