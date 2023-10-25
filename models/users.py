import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import google.cloud.logging

class Users():
    
    def __init__(self, data,db):
        self.logger = logging.getLogger('weblog').getChild("uers")
        self.logger.setLevel(logging.DEBUG)
        client = google.cloud.logging.Client()
        client.setup_logging()
        self.data = data
        self.db = db
        

    def insert(self,db,collection_name):

        try:

            self.logger.info(self.db)
            self.logger.info("--insert start--")
            db.collection(collection_name).document().set(self.data)
            self.logger.info("--insert end--")
        except Exception as e:
            self.logger.error(e)
            raise
        
    # TODO:validation check
    # def validation_data(self,data):
    #     if data