import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import google.cloud.logging

class Users():
    
    def __init__(self, db, jdata):
        self.logger = logging.getLogger('weblog').getChild("users")
        client = google.cloud.logging.Client()
        client.setup_logging()

        self.db = db        
        self.data = {
            "contact_key": jdata['contact_key'],
            "uid": jdata['uid'],
            "acid": jdata['acid'],
            "campaign_id": jdata['campaign_id'],
            "content_id": jdata['content_id'],
            "send_flg": False
        }
        

    def insert(self,collection_name):

        try:
            self.logger.info("--insert start u--")
            self.db.collection(collection_name).add(self.data)
            self.logger.info("--insert end u--")
        except Exception as e:
            self.logger.error(e)
            raise
        
    # TODO:validation check
    # def validation_data(self,data):
    #     if data