import psycopg2, os, sys, cv2, numpy as np
from timeit import default_timer as timer

sys.path.append('../../src/persistance')
sys.path.append('../../src/logic/trainingServer')
sys.path.append('../../src/persistance/seed')

from dbAdapter import DBAdapter
from dbQueries import DBQueries
from training import Trainer
from seed import seedDB


#-------------------------------------
#testDB (class)
#
#This class tests 2 different configerations for the databases
#In the first configeration, the data is stored in 3 seperate databses
#In the second configeration, the data is stored in a single database
#This class tests which configeration is faster
#-------------------------------------
class testdb:
    
    def __init__(self) -> None:
        self.adapter = DBAdapter()
        self.queries = DBQueries()
        self.trainingPath = '../../res/trainingData/'
        self.testing_path = '../../res/testingData/'
        self.model = Trainer(height = 80, width = 70, num_images=320, img_path=self.trainingPath)
        self.model.run_training()
        self.img = None

    #-------------------------------------
    #run_test_3db(self,)
    #
    #This methods connects to each of the 3 databases
    #and send an image vector as input to a user stored
    #function, and prints the results
    #-------------------------------------
    def run_test_3db(self,):
        conA = self.adapter.connect_to_DBA()
        conB = self.adapter.connect_to_DBB()
        conC = self.adapter.connect_to_DBC()

        resultA = self.queries.mapDB(conA, self.img)
        resultB = self.queries.mapDB(conB, self.img)
        resultC = self.queries.mapDB(conC, self.img)

        self.adapter.close_DBA()
        self.adapter.close_DBB()
        self.adapter.close_DBC()

        print(resultA)
        print(resultB)
        print(resultC)

    #-------------------------------------
    #run_test_1db(self,)
    #
    #This methods connects to the first database
    #and send a an image vector to a user stored
    #function and prints the result
    #-------------------------------------
    def run_test_1db(self,):

        conA = self.adapter.connect_to_DBA()
        resultA = self.queries.mapDB(conA, self.img)
        print(resultA)
        self.adapter.close_DBA()

    #-------------------------------------
    #process_image(self, path)
    #
    #   path: path of the image being processed
    #
    #This function takes an input image, reads
    #it as a grayscale image and converts it to an
    #image vector and performs basic calculations
    #-------------------------------------
    def process_image(self,path):
        
        img = cv2.imread(path, 0)
        img_col = np.array(img, dtype='float64').flatten() 
        img_col -= self.model.mean_vector
        img_col = np.reshape(img_col, (70*80, 1))  
        S = self.model.eVectors * img_col

        processed_image = S.reshape((1,len(S)))
        processed_image = str(processed_image.tolist())[1:-1]
        
        return processed_image

    #-------------------------------------
    #run_tests(self,)
    #
    #This function runs the 3db test and
    #the 1 db test and tracks their time
    #-------------------------------------
    def run_tests(self, ):
        self.img = self.process_image(self.testing_path+'10_1.jpg')
        
        response = input("Make sure all 3 dbs are seeded using the seed.py file. \nType <yes> when done:")
        while response != 'yes':
            response = input("Make sure all 3 dbs are seeded using the seed.py file. \nType <yes> when done: ")

        #run timer for 3 dbs
        start = timer()
        self.run_test_3db()
        end = timer()

        print(f'Time: {end-start} secs, with 3 databses')

        response = input("Make sure dbA is seeded using the badSeed.py file. \nType <yes> when done:")
        while response != 'yes':
            response = input("Make sure dbA is seeded using the badSeed.py file. \nType <yes> when done:")
        
        start = timer()
        self.run_test_1db()
        end = timer()

        print(f'Time: {end-start} secs, with 1 database')

if __name__ == '__main__':
    test = testdb()
    test.run_tests()