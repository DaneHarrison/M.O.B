# --------------------------------
# badSeed (class)
#
# badSeed is responsible for connecting to face database DBA with all faces for testing purposes
# --------------------------------
from seed import seedDB

class BadSeed(seedDB):

# --------------------------------
# seed
# Responsible for connecting to face database DBA with all faces for testing purposes
# --------------------------------
    def seed(self,):
        self.run_seed(start = 0, end = 320, port = 5432)
        print("Database A seeded successfully!")


if __name__ == '__main__':
    s = BadSeed()
    s.seed()