import dbAdapter, asyncio, json

person = 0
index = 0 

def main():
    namesFile = open("./src/persistance/faceDB/seed/randomNames.json", "r")
    photosFile = open("./src/persistance/faceDB/seed/fileManifest.json", "r")
    weightsFile = open("./src/persistance/faceDB/seed/weights.json", "r")

    names = json.loads(namesFile.read())
    photos = json.loads(photosFile.read())
    weights = json.loads(weightsFile.read())
    adapter = dbAdapter()

    proceed = seedA(adapter, names, weights, photos)
    if(proceed):
        proceed = seedB(adapter, names, weights, photos)
    if(proceed):
        proceed = seedC(adapter, names, weights, photos)

    namesFile.close()
    photosFile.close()
    weightsFile.close()

    if(proceed):
        print("\n[SUCCESS] all databases have been seeded...")
    else:
        print("\n[ERROR] problem encoutered while seeding databases...")


def seedA(adapter, names, weights, photos):
    print("Loading Database A...")
    db = adapter.getDBA()
    
    return seed(db, names, weights, photos)
    
def seedB(adapter, names, weights, photos):
    print("Loading Database B...")
    db = adapter.getDBB()
    
    return seed(db, names, weights, photos)

def seedC(adapter, names, weights, photos):
    print("Loading Database C...")
    db = adapter.getDBC()
    
    return seed(db, names, weights, photos)

async def seed(db, names, weights, photos) -> None:
    await db.connect()
    proceed = true
    
    for i in range(0, 100):
        proceed = await db.user.create( data = {
            'Name': names[person],
            'Weight': weights[index],
            'Photo': photos[index]
        })

        index +=1
        if(index is not 0 and index % 8 == 0):  # since every user has 8 training photos each 8th photo is a new person
            person += 1
        if(not user or index >= len(photos)):
            break
    
    await db.disconnect()

    return proceed


if __name__ == '__main__':
    main()