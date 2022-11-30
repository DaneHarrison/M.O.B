# --------------------------------
# seed (script)
#
# Fills our face databases with their respective data
#   - ID        (int) - determined automatically by database
#   - Name      (string)
#   - Weight    (Int[])
#   - Photo     (String)
#
# NOTE: all seeding should be started from inside the seed directory
# --------------------------------
import json, sys, json
from seedGlobals import SeedGlobals

sys.path.append('../../')
from dbAdapter import DBAdapter

NAMES_LOCATION = './randomNames.json'                       # Holds the location of where all seed names are stored [string[]]
WEIGHTS_LOCATION = './weights.json'                         # Holds the location of where all seed weights are stored [int[][]]
PHOTO_PATH_LOCATION = './fileManifest.json'                 # Holds the location of where all seed photo paths are stored [string[]]
TRAINING_PHOTO_LOCATION = '../../../../res/trainingData/'   # Holds the location of where all the training images are stored

def main():
    # Loads then closes the names, weights and photo paths required for initial datbase seeding
    with open(NAMES_LOCATION, 'r') as names_file:
        names = json.load(names_file)
    with open(WEIGHTS_LOCATION, 'r') as weights_file:
        weights = json.load(weights_file)
    with open(PHOTO_PATH_LOCATION, 'r') as photo_path_files:
        photo_paths = json.load(photo_path_files)

    adapter = DBAdapter()                       # Holds references to the databases we would like to seed
    global_vars = SeedGlobals()                 # Holds an instance of our global variables (prisma does not play nice)
    is_seeded = already_Seeded(names, adapter)  # A boolean that determines if we have already seeded the databases

    if(is_seeded):   # Dont do anything... its seeded already
        print("[ERROR] database is already seeded")
    else:            # Time to start seeding!
        # If there is an error encountered while seeding, the process will stop and it will be reported
        proceed = seed_A(adapter, global_vars, names, weights, photo_paths)
        if(proceed):
            proceed = seed_B(adapter, global_vars, names, weights, photo_paths)
        if(proceed):
            proceed = seed_C(adapter, global_vars, names, weights, photo_paths)

        if(proceed):    # All data was successfully seeded
            print("\n[SUCCESS] all databases have been seeded...")
        else:           # Some piece of data failed to be seeded
            print("\n[ERROR] problem encoutered while seeding databases...")


# --------------------------------
# seed_A
# Seeds face database DBA
#
# Parameters:
# adapter: Holds references to the databases we would like to seed
# global_vars: Holds an instance of our global variables (prisma does not play nice)
# names: Holds a string list of names for all users
# weights: Holds a int[] list of all the weights assocaited with a users face
# photo_paths: Holds a string list containing the paths to all the photos we'd like to load
#
# Returns:
# A boolean representing if the seeding process was successful
# --------------------------------
def seed_A(adapter, global_vars, names, weights, photo_paths):
    print("Loading Database A...")
    db = adapter.get_DBA()
    
    return seed(db, global_vars, names, weights, photo_paths, 100)
    
# --------------------------------
# seed_B
# Seeds face database DBB
#
# Parameters:
# adapter: Holds references to the databases we would like to seed
# global_vars: Holds an instance of our global variables (prisma does not play nice)
# names: Holds a string list of names for all users
# weights: Holds a int[] list of all the weights assocaited with a users face
# photo_paths: Holds a string list containing the paths to all the photos we'd like to load
#
# Returns:
# A boolean representing if the seeding process was successful
# --------------------------------
def seed_B(adapter, global_vars, names, weights, photo_paths):
    print("Loading Database B...")
    db = adapter.get_DBB()
    
    return seed(db, global_vars, names, weights, photo_paths, 100)

# --------------------------------
# seed_C
# Seeds face database DBC
#
# Parameters:
# adapter: Holds references to the databases we would like to seed
# global_vars: Holds an instance of our global variables (prisma does not play nice)
# names: Holds a string list of names for all users
# weights: Holds a int[] list of all the weights assocaited with a users face
# photo_paths: Holds a string list containing the paths to all the photos we'd like to load
#
# Returns:
# A boolean representing if the seeding process was successful
# --------------------------------
def seed_C(adapter, global_vars, names, weights, photo_paths):
    print("Loading Database C...")
    db = adapter.get_DBC()
    
    return seed(db, global_vars, names, weights, photo_paths, 150)

# --------------------------------
# already_seeded
# Identifies if the databases have already been seeded
#
# Parameters:
# adapter: Holds references to the databases we would like to seed
#
# Returns:
# The results of the query: None if no users are present or the information pertaining to existing users
# --------------------------------
def already_seeded(adapter) -> None:
    db = adapter.get_DBA()
    db.connect()

    results = db.user.find_many() # Checks if there are any users stored in the databases
    db.disconnect()

    return results

# --------------------------------
# seed
# Seeds a database
#
# Parameters:
# db: Holds a references to the database we would like to seed
# global_vars: Holds an instance of our global variables (prisma does not play nice)
# names: Holds a string list of names for all users
# weights: Holds a int[] list of all the weights assocaited with a users face
# photo_paths: Holds a string list containing the paths to all the photos we'd like to load
# max_photos: The maximum number of photos we should be storing in a given database
#
# Returns:
# A boolean representing if the procedure was successful
# --------------------------------
def seed(db, global_vars, names, weights, photo_paths, max_photos) -> None:
    db.connect()

    # For each database, store their users and information
    for i in range(0, max_photos):
        proceed = db.user.create( data = {
            'Name': names[global_vars.get_person()],
            'Weight': weights[global_vars.get_index()],
            'Photo': str(open(TRAINING_PHOTO_LOCATION + photo_paths[global_vars.get_index()], "rb").read()),
        })

        global_vars.incr_index()
        global_vars.check_incr_person()   # The person should change every 8 photos
        if(not proceed or global_vars.get_index() >= len(photo_paths)): # If we've run out of photos or an error is encountered, stop
            break
    
    db.disconnect()

    return proceed


if __name__ == '__main__':
    main()