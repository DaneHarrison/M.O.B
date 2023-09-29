import psycopg2
import json
from dotenv import load_dotenv

class seedDB:
    def __init__(self, testPath="") -> None:
        '''
        seed (class)

        Responsible for connecting to each database and seeding the initial data
        '''
        load_dotenv()           # Loads the .env file

        #location of the random names
        self.names_location = testPath + 'randomNames.json'

        #location of the weights matrix
        self.weights_location = testPath + 'weights.json'

        #location of the phots manifest
        self.photo_path_location = testPath + 'fileManifest.json'

        #location of the training images
        self.training_photo_location = testPath + '../../../data/trainingData/'

        #load all of the names
        with open(self.names_location, 'r') as names_file:
            self.names = json.load(names_file)

        #load the weights matrix
        with open(self.weights_location, 'r') as weights_file:
            self.weights = json.load(weights_file)

        #load the paths of all the photos
        with open(self.photo_path_location, 'r') as photo_path_files:
            self.photo_paths = json.load(photo_path_files)

        self.name_idx = 0

    def run_seed(self, start, end, port):
        '''
        Connects to each of the databases and seeds them with default data

        Parameters:
            start (int): starting index of the photos
            end (int): ending index of the photos
            port (int): connection port for the database
        '''
        #connection string
        con = psycopg2.connect(
            host='localhost',
            port=port,
            database='MOB',
            user='user',
            password='password'
        )

        cur = con.cursor() #create a cursor in the database

        id_start = 0 #initialize the id index

        for i in range(start, end):
            
            #every 8 photos, increase the name index
            #so the next 8 photos are labeled with a
            #different name
            if i % 8 == 0:
                self.name_idx += 1
            
            #get the ith weight column from the weight matrix
            my_weights = self.weights[i]

            #read the photo as binary
            my_photo = open(self.training_photo_location + self.photo_paths[i], "rb")
            my_photo = psycopg2.Binary(my_photo.read())

            #build the insert query
            my_msg = f"BEGIN; insert into public.\"UserFaces\" values ({id_start}, '{self.names[self.name_idx]}', ARRAY{my_weights}, {my_photo}); COMMIT;"
            id_start += 1
            
            #execute the insert query
            cur.execute(my_msg)

        cur.close()  #close the cursor
        con.close()  #close the connection

# --------------------------------
# seed
# Responsible for connecting to each database and seeding the initial data.
# --------------------------------
    def seed(self,):
        self.run_seed(start = 0, end = 104, port = 5432)
        print("Database A seeded successfully!")
        self.run_seed(start = 104, end = 208, port = 5433)
        print("Database B seeded successfully!")
        self.run_seed(start = 208, end = 320, port = 5434)
        print("Database C seeded successfully!")

if __name__ == '__main__':
    s = seedDB()
    s.seed()