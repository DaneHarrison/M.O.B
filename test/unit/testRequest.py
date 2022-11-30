import unittest

class Requests(unittest.TestCase):
    def test_default_values(self):
        hi = 'hi'
        self.assertEqual(hi, 'hi')
        assert hi == 'hi'
# default values


# compute_image_vector


# calc_min_query_details
    # basic
        #-smallest to littlelest 
    # complex
        #-mixed order
        #-float included
    # empty
        #-None
    # edge
        #-same distance

    # def calc_min_query_details(self, distances):
    #     distances = [self.res_DBA.Distance, self.res_DBB.Distance, self.res_DBC.Distance]
    #     min_index = distances.index(min(distances))  

    #     # Check which index was the smallest, that is the ID and database we want
    #     if(min_index == 0):      # Choose database A
    #         query_details = (self.res_DBA.ID, self.dbAdapter.get_DBA())
    #     elif(min_index == 1):    # Choose database B
    #         query_details = (self.res_DBB.ID, self.dbAdapter.get_DBB())
    #     else:                   # Choose database C
    #         query_details = (self.res_DBC.ID, self.dbAdapter.get_DBC())

    #     return query_details

if __name__ == '__main__':
    import nose2
    nose2.main()  