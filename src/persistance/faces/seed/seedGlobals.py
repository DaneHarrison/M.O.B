# --------------------------------
# seedGlobals (class)
#
# Prisma has a problem global variables, so this class is used to simplify how entries are entered and tracked
# --------------------------------
class SeedGlobals:
    def __init__(self):
        self.index = 0      # keeps track of how many users have already been entered [0, 320)
        self.person = 0     # keeps track of what person this photo belongs to (each user has 8 photos)


# --------------------------------
# incr_index
# Increments the count of how many users have been entered [0, 320)
# --------------------------------    
    def incr_index(self):
        self.index += 1

# --------------------------------
# get_index
# Getter that returns the current index count
# 
# Returns:
# An integer representing the current index count
# --------------------------------  
    def get_index(self):
        return self.index

# --------------------------------
# check_incr_person
# Determines whether we should change the current user or not (each user has 8 photos)
# --------------------------------
    def check_incr_person(self):
        if(self.index != 0 and self.index % 8 == 0):
            self.person += 1

# --------------------------------
# get_person
# Getter that returns the current person
# 
# Returns:
# An integer representing the current person 
# --------------------------------             
    def get_person(self):
        return self.person