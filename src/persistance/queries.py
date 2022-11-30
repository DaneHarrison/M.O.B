class Queries:
    def mapDB(self, db) -> None: # here we need the index [ID] and a distance [Distance]
        db.connect()
        
        # ...

        db.disconnect()

    def reduceDB(self, queryDetails) -> None: # here we want a name [Name] and a picture [Photo]
        db.connect()
        
        # ...

        db.disconnect()

    def checkForPrevEntry(photo, database) -> None:
        database.connect()
        found = database.entry.find_unique( where = {'Photo': photo})
        database.disconnect()

        return found

    def addEntry(photo, database) -> None:
        database.connect()
        database.entry.create( data = {'Photo': photo})
        database.disconnect()