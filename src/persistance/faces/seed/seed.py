import psycopg2
import json

class seeddb:
    def __init__(self) -> None:
        self.names_location = './randomNames.json'
        self.weights_location = './weights.json'
        self.photo_path_location = './fileManifest.json'
        self.training_photo_location = '../../../../res/trainingData/'

        with open(self.names_location, 'r') as names_file:
            self.names = json.load(names_file)

        with open(self.weights_location, 'r') as weights_file:
            self.weights = json.load(weights_file)

        with open(self.photo_path_location, 'r') as photo_path_files:
            self.photo_paths = json.load(photo_path_files)

        self.name_idx = 0

    def run_seed(self, start, end, port):
        con = psycopg2.connect(
            host='localhost',
            port=port,
            database='MOB',
            user='user',
            password='password'
        )

        cur = con.cursor()
        id_start = 0
        for i in range(start, end):
            
            if i % 8 == 0:
                self.name_idx += 1
            
            my_weights = self.weights[i]
            for j in range(len(my_weights)):
                my_weights[j] = int(my_weights[j])

            my_photo = open(self.training_photo_location + self.photo_paths[i], "rb")
            my_photo = psycopg2.Binary(my_photo.read())

            my_msg = f"BEGIN; insert into public.\"UserFaces\" values ({id_start}, '{self.names[self.name_idx]}', ARRAY{my_weights}, {my_photo}); COMMIT;"
            id_start += 1
            
            cur.execute(my_msg)
        cur.execute("CREATE EXTENSION plpython3u;")
        cur.close()
        con.close()


    def seed(self,):
        self.run_seed(start = 0, end = 104, port = 5432)
        print("Database A seeded successfully!")
        self.run_seed(start = 104, end = 208, port = 5433)
        print("Database B seeded successfully!")
        self.run_seed(start = 208, end = 320, port = 5434)
        print("Database C seeded successfully!")


if __name__ == '__main__':

    s = seeddb()
    s.seed()


