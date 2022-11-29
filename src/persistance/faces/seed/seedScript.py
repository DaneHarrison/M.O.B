import json, sys, json
from seedGlobals import SeedGlobals

sys.path.append('../../')
from dbAdapter import DBAdapter


def main():
    namesFile = open("./randomNames.json", "r")
    photosFile = open("./fileManifest.json", "r")
    weightsFile = open("./weights.json", "r")

    names = json.loads(namesFile.read())
    photos = json.loads(photosFile.read())
    weights = json.loads(weightsFile.read())

    adapter = DBAdapter()
    globalVars = SeedGlobals()
    isSeeded = alreadySeeded(names, adapter)

    if(isSeeded):
        print("[ERROR] database is already seeded")
    else:
        proceed = seedA(adapter, globalVars, names, weights, photos)
        if(proceed):
            proceed = seedB(adapter, globalVars, names, weights, photos)
        if(proceed):
            proceed = seedC(adapter, globalVars, names, weights, photos)

        namesFile.close()
        photosFile.close()
        weightsFile.close()

        if(proceed):
            print("\n[SUCCESS] all databases have been seeded...")
        else:
            print("\n[ERROR] problem encoutered while seeding databases...")


def seedA(adapter, globalVars, names, weights, photos):
    print("Loading Database A...")
    db = adapter.getDBA()
    
    return seed(db, globalVars, names, weights, photos)
    
def seedB(adapter, globalVars, names, weights, photos):
    print("Loading Database B...")
    db = adapter.getDBB()
    
    return seed(db, globalVars, names, weights, photos)

def seedC(adapter, globalVars, names, weights, photos):
    print("Loading Database C...")
    db = adapter.getDBC()
    
    return seed(db, globalVars, names, weights, photos)

def alreadySeeded(names, adapter) -> None: ## do one here so it checks which ones need to be seeded
    db = adapter.getDBA()
    db.connect()

    results = db.user.find_many()

    db.disconnect()

    return results

def seed(db, globalVars, names, weights, photos) -> None:
    db.connect()

    for i in range(0, 100):
        proceed = db.user.create( data = {
            'Name': names[globalVars.getPerson()],
            'Weight': weights[globalVars.getIndex()],
            'Photo': str(open("../../../../res/trainingData/" + photos[globalVars.getIndex()], "rb").read()),
        })

        globalVars.incrIndex()
        globalVars.checkIncrPerson()
        if(not proceed or globalVars.getIndex() >= len(photos)):
            break
    
    db.disconnect()

    return proceed


if __name__ == '__main__':
    main()