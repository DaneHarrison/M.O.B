import unittest, sys

sys.path.append('../../src/persistance')

from dbAdapter import DBAdapter

class Seed(unittest.TestCase):
    def getResults(self, currDB):
        currDB.connect()
        results = currDB.user.find_many()
        currDB.disconnect()

        return results

    def test_seed(self):
        adapter = DBAdapter()
        currDB = None
        merged = {}

        resultsA = self.getResults(adapter.get_DBA())
        resultsB = self.getResults(adapter.get_DBB())
        resultsC = self.getResults(adapter.get_DBC())

        self.assertEqual(len(resultsB), 100)
        self.assertEqual(len(resultsA), 100)
        self.assertEqual(len(resultsC), 120)

        for result in resultsA:
            self.assertTrue(instanceof(result["userID"], int))
            self.assertGreaterEqual(result["userID"], 0)

            self.assertTrue(instanceof(result["userID"], []))
            self.assertGreaterEqual(len(result["userWeight"]), 0)

            self.assertTrue(instanceof(result["Name"], str))
            self.assertTrue(instanceof(result["Photo"], str))

        for result in resultsB:
            self.assertTrue(instanceof(result.ID, int))
            self.assertGreaterEqual(result.ID, 0)

            self.assertTrue(instanceof(result.ID, []))
            self.assertGreaterEqual(len(result.Weight), 0)

            self.assertTrue(instanceof(result.Name, str))
            self.assertTrue(instanceof(result.Photo, str))

        for result in resultsC:
            self.assertTrue(instanceof(result.ID, int))
            self.assertGreaterEqual(result.ID, 0)

            self.assertTrue(instanceof(result.ID, []))
            self.assertGreaterEqual(len(result.Weight), 0)

            self.assertTrue(instanceof(result.Name, str))
            self.assertTrue(instanceof(result.Photo, str))

        merged.update(resultsA)
        merged.update(resultsB)
        merged.update(resultsC)

        # 40 people 8 images each
        for i in range(0, 40):
            currName = merged[i*8].Name
            for j in range(0, 8):
                self.assertTrue(merged[i*8 + j].Name == currName)

        photos = set()
        weights = set()
        for result in merged:
            photos.add(result.Photo)
            weights.add(results.Weight)

        self.assertEqual(len(photos), 320)
        self.assertEqual(len(weights), 320)


if __name__ == '__main__':
    import nose2
    nose2.main()  