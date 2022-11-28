import asyncio

class Queries:
    async def mapDB(self, db) -> None: # here we need the index [ID] and a distance [Distance]
        await db.connect()
        
        # ...

        await db.disconnect()

    async def reduceDB(self, db) -> None: # here we want a name [Name] and a picture [Photo]
        await db.connect()
        
        # ...

        await db.disconnect()