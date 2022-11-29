import asyncio

class Queries:
    async def mapDB(self, db) -> None: # here we need the index [ID] and a distance [Distance]
        await db.connect()
        
        # ...

        await db.disconnect()

    async def reduceDB(self, queryDetails) -> None: # here we want a name [Name] and a picture [Photo]
        await db.connect()
        
        # ...

        await db.disconnect()

    async def checkForPrevEntry(photo, database) -> None:
        await database.connect()
        found = await database.entry.find_unique( where = {'Photo': photo})
        await database.disconnect()

        return found

    async def addEntry(photo, database) -> None:
        await database.connect()
        await database.entry.create( data = {'Photo': photo})
        await database.disconnect()