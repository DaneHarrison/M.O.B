from src.persistance.adapter import Adapter
from src.persistance.queries import Queries
from src.logic.eigRequest import EigRequest
from dotenv import load_dotenv
import os


class Logic:
    def __init__(self):
        load_dotenv()       # Loads the .env file

        # Create connections to face databases dbA, dbB, dbC and logs
        self.dbA = Adapter(os.getenv('A_DB'), os.getenv('A_HOST'), os.getenv('A_PORT'), os.getenv('A_USER'), os.getenv('A_PASS'))
        self.dbB = Adapter(os.getenv('B_DB'), os.getenv('B_HOST'), os.getenv('B_PORT'), os.getenv('B_USER'), os.getenv('B_PASS'))
        self.dbC = Adapter(os.getenv('C_DB'), os.getenv('C_HOST'), os.getenv('C_PORT'), os.getenv('C_USER'), os.getenv('C_PASS'))
        self.logs = Adapter(os.getenv('LOGS_DB'), os.getenv('LOGS_HOST'), os.getenv('LOGS_PORT'), os.getenv('LOGS_USER'), os.getenv('LOGS_PASS'))

        self.faceQuerier = FaceQueries()
        self.logQuerier = LogQueries()

        self.connToLogs = logs.connect()
        self.faceConns = [
            self.dbA.connect(),
            self.dbB.connect(),
            self.dbC.connect(),
        ]


    def runEigenFace(self, img):
        req = EigRequest(self.faceQuerier, self.faceConns)
        results = None

        if self.logQuerier.recordIfNewImage(img, self.connToLogs):
            image = req.prepareInput(img)
            image_vector = req.compute_image_vector()
            
            mappings = req.map(self.faceQuerier, self.faceConns)
            bestMapping = req.chooseLeast()
            results = req.reduce(self.faceQuerier, self.faceConns)
            results = req.formatOutput(mappings, results)

        return results