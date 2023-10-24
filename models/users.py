import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import google.cloud.logging

class Users():
    
    def __init__(self,data):
        self.logger = logging.getLogger('weblog')
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("init start")
        self.db = firestore.Client()
        print("create db")
        
        self.data = data
        print("init end")
        

    def insert(self,collection_name):
        self.logger.info(collection_name)
        print("------insert data------")
        print(self.data)
        self.db.collection(collection_name).document().set(self.data)
        
    # TODO:validation check
    # def validation_data(self,data):
    #     if data