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

    async def checkForPrevEntry() -> None:
        await db.connect()
        
        # ...

        await db.disconnect()

    async def addEntry() -> None:
        await db.connect()
        
        # ...

        await db.disconnect()