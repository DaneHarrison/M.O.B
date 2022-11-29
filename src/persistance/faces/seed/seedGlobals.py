class SeedGlobals:
    def __init__(self):
        self.index = 0
        self.person = 0

    
    def incrIndex(self):
        self.index += 1

    def getIndex(self):
        return self.index

    def checkIncrPerson(self):
        if(self.index != 0 and self.index % 8 == 0):  # since every user has 8 training photos each 8th photo is a new person
            self.person += 1
            
    def getPerson(self):
        return self.person