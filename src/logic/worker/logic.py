from persistance.adapter import Adapter
from persistance.faceQueries import FaceQueries
from persistance.logQueries import LogQueries
from logic.worker.eigRequest import EigRequest
from typing import Optional
from collections import namedtuple
from dotenv import load_dotenv
import os

EigResult = namedtuple('EigResult', ['Name', 'Dist', 'Photo', 'MeanFace'])

class Logic:
    def __init__(self):
        load_dotenv()       # Loads the .env file

        # Create connections to face databases dbA, dbB, dbC and logs
        self.faceQuerier = FaceQueries()
        self.logQuerier = LogQueries()

        self.logs = Adapter(os.getenv('LOGS_DB'), os.getenv('LOGS_HOST'), os.getenv('LOGS_PORT'), os.getenv('LOGS_USER'), os.getenv('LOGS_PASS'))
        self.faces = [
            Adapter(os.getenv('A_DB'), os.getenv('A_HOST'), os.getenv('A_PORT'), os.getenv('A_USER'), os.getenv('A_PASS')),
            Adapter(os.getenv('B_DB'), os.getenv('B_HOST'), os.getenv('B_PORT'), os.getenv('B_USER'), os.getenv('B_PASS')),
            Adapter(os.getenv('C_DB'), os.getenv('C_HOST'), os.getenv('C_PORT'), os.getenv('C_USER'), os.getenv('C_PASS'))
        ]


    def runEigenFace(self, img: bytes) -> Optional[EigResult]:
        req = EigRequest()
        results = None

        if img and self.logQuerier.recordIfNewImage(img, self.logs):
            img = req.prepareInput(img)
            image_vector = req.compute_image_vector(img)
            
            mappings = req.mapDB(image_vector, self.faces, self.faceQuerier)
            bestMapping = req.chooseBest(mappings)
            reducedResults = req.reduceDB(bestMapping, self.faceQuerier)
        
            if reducedResults:
                results = EigResult(
                    Name=reducedResults.Name, 
                    Dist=bestMapping.Dist, 
                    Photo=reducedResults.Photo, 
                    MeanFace=req.getMeanVectorBytes()
                ) 

        return results