import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import google.cloud.logging

class Users():
    
    def __init__(self, db, data):
        self.logger = logging.getLogger('weblog').getChild("uers")
        self.logger.setLevel(logging.DEBUG)
        client = google.cloud.logging.Client()
        client.setup_logging()
        self.logger.info("init start")
        self.db = db
        self.data = data


    def insert(self,collection_name):

        try:
            self.logger.info(collection_name)
            self.logger.info(self.data)

            self.db.collection(collection_name).document().set(self.data)

        except Exception as e:
            self.logger.error(e)
            raise
        
    # TODO:validation check
    # def validation_data(self,data):
    #     if data