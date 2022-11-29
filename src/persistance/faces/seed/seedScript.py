import asyncio, json, sys, json
from seedGlobals import SeedGlobals

sys.path.append('../../')
from dbAdapter import DBAdapter

async def main() -> None:
    namesFile = open("./randomNames.json", "r")
    photosFile = open("./fileManifest.json", "r")
    weightsFile = open("./weights.json", "r")

    names = json.loads(namesFile.read())
    photos = json.loads(photosFile.read())
    weights = json.loads(weightsFile.read())

    adapter = DBAdapter()
    globalVars = SeedGlobals()
    isSeeded = await alreadySeeded(names, adapter)

    if(isSeeded):
        print("[ERROR] database is already seeded")
    else:
        proceed = await seedA(adapter, globalVars, names, weights, photos)
        if(proceed):
            proceed = await seedB(adapter, globalVars, names, weights, photos)
        if(proceed):
            proceed = await seedC(adapter, globalVars, names, weights, photos)

        namesFile.close()
        photosFile.close()
        weightsFile.close()

        if(proceed):
            print("\n[SUCCESS] all databases have been seeded...")
        else:
            print("\n[ERROR] problem encoutered while seeding databases...")


async def seedA(adapter, globalVars, names, weights, photos):
    print("Loading Database A...")
    db = adapter.getDBA()
    
    return await seed(db, globalVars, names, weights, photos)
    
async def seedB(adapter, globalVars, names, weights, photos):
    print("Loading Database B...")
    db = adapter.getDBB()
    
    return await seed(db, globalVars, names, weights, photos)

async def seedC(adapter, globalVars, names, weights, photos):
    print("Loading Database C...")
    db = adapter.getDBC()
    
    return await seed(db, globalVars, names, weights, photos)

async def alreadySeeded(names, adapter) -> None: ## do one here so it checks which ones need to be seeded
    db = adapter.getDBA()
    await db.connect()

    results = await db.user.find_many()

    await db.disconnect()

    return results

async def seed(db, globalVars, names, weights, photos) -> None:
    await db.connect()

    for i in range(0, 100):
        proceed = await db.user.create( data = {
            'Name': names[globalVars.getPerson()],
            'Weight': weights[globalVars.getIndex()],
            'Photo': str(open("../../../../res/trainingData/" + photos[globalVars.getIndex()], "rb").read()),
        })

        globalVars.incrIndex()
        globalVars.checkIncrPerson()
        if(not proceed or globalVars.getIndex() >= len(photos)):
            break
    
    await db.disconnect()

    return proceed


if __name__ == '__main__':
    asyncio.run(main())