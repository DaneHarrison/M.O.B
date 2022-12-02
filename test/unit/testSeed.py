import unittest, psycopg2, sys, os, nose2

sys.path.append('../../src/persistance/seed/')

from seed import seedDB
from dotenv import load_dotenv

class Seed(unittest.TestCase):
    def clearDB(self, port):
        con = psycopg2.connect(host=os.getenv('HOST'), port=port, database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("BEGIN; TRUNCATE TABLE public.\"UserFaces\"; COMMIT;")
        cur.execute("DROP EXTENSION plpython3u;")

        cur.close()
        con.close()

    def test_seed_default_values(self):
        seeder = seedDB('../../src/persistance/seed/')

        self.assertEqual(seeder.names_location, '../../src/persistance/seed/randomNames.json')
        self.assertEqual(seeder.weights_location, '../../src/persistance/seed/weights.json')
        self.assertEqual(seeder.photo_path_location, '../../src/persistance/seed/fileManifest.json')
        self.assertEqual(seeder.training_photo_location, '../../src/persistance/seed/../../../res/trainingData/')
        
        self.assertTrue(os.path.exists(seeder.names_location))
        self.assertTrue(os.path.exists(seeder.weights_location))
        self.assertTrue(os.path.exists(seeder.photo_path_location))

        self.assertEqual(seeder.name_idx, 0)
        self.assertEqual(len(seeder.names), 49)
        self.assertEqual(len(seeder.weights), 320)
        self.assertEqual(len(seeder.photo_paths), 320)

        for name in seeder.names:
            self.assertTrue(isinstance(name, str))

        for weight in seeder.weights:
            self.assertEquals(len(weight), 136)

        for path in seeder.photo_paths:
            self.assertTrue(os.path.exists(seeder.training_photo_location + path))
            self.assertTrue(isinstance(path, str))


    def test_seed_A(self):
        seeder = seedDB('../../src/persistance/seed/')

        self.clearDB(os.getenv('DB_A_PORT'))
        self.clearDB(os.getenv('DB_B_PORT'))
        self.clearDB(os.getenv('DB_C_PORT'))

        seeder.seed()

        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_A_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("select * from public.\"UserFaces\"")
        results = cur.fetchall()
        cur.close()
        con.close()

        index = 0
        person = 0
        for row in results:
            if(index%8 == 0):
                person += 1

            self.assertEquals(row[0], index)
            self.assertEquals(row[1], seeder.names[person])
            self.assertEquals(row[2], seeder.weights[index])

            index += 1
        
        self.assertEqual(len(results), 104)

    def test_seed_B(self):
        seeder = seedDB('../../src/persistance/seed/')

        self.clearDB(os.getenv('DB_A_PORT'))
        self.clearDB(os.getenv('DB_B_PORT'))
        self.clearDB(os.getenv('DB_C_PORT'))

        seeder.seed()

        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_B_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("select * from public.\"UserFaces\"")
        results = cur.fetchall()
        cur.close()
        con.close()

        index = 104
        person = 13
        for row in results:
            if(index%8 == 0):
                person += 1
            self.assertEquals(row[0], index - 104)
            self.assertEquals(row[1], seeder.names[person])
            self.assertEquals(row[2], seeder.weights[index])

            index += 1
        
        self.assertEqual(len(results), 104)


    def test_seed_C(self):
        seeder = seedDB('../../src/persistance/seed/')

        self.clearDB(os.getenv('DB_A_PORT'))
        self.clearDB(os.getenv('DB_B_PORT'))
        self.clearDB(os.getenv('DB_C_PORT'))

        seeder.seed()

        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_C_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("select * from public.\"UserFaces\"")
        results = cur.fetchall()
        cur.close()
        con.close()

        index = 208
        person = 26
        for row in results:
            if(index%8 == 0):
                person += 1
            self.assertEquals(row[0], index - 208)
            self.assertEquals(row[1], seeder.names[person])
            self.assertEquals(row[2], seeder.weights[index])

            index += 1
        
        self.assertEqual(len(results), 112)
    

    def test_unique_photos_and_weights(self):
        seeder = seedDB('../../src/persistance/seed/')
        weights = set()
        photos = set()

        self.clearDB(os.getenv('DB_A_PORT'))
        self.clearDB(os.getenv('DB_B_PORT'))
        self.clearDB(os.getenv('DB_C_PORT'))

        seeder.seed()

        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_A_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("select * from public.\"UserFaces\"")
        results = cur.fetchall()
        cur.close()
        con.close()

        for row in results:
            weights.add(''.join(str(e) for e in row[2]))
            photos.add(row[3])

        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_B_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("select * from public.\"UserFaces\"")
        results = cur.fetchall()
        cur.close()
        con.close()

        for row in results:
            weights.add(''.join(str(e) for e in row[2]))
            photos.add(row[3])

        con = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('DB_C_PORT'), database=os.getenv('DB'), user=os.getenv('USER'),password=os.getenv('PASSWORD'))
        cur = con.cursor()

        cur.execute("select * from public.\"UserFaces\"")
        results = cur.fetchall()
        cur.close()
        con.close()

        for row in results:
            weights.add(''.join(str(e) for e in row[2]))
            photos.add(row[3])

        self.assertEqual(len(photos), 320)
        self.assertEqual(len(weights), 320)


if __name__ == '__main__':
    load_dotenv()           # Loads the .env file
    nose2.main()  