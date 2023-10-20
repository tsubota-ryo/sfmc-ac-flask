import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Users():
    
    def __init__(self):
        self.db = firestore.Client()
        
    def get_documents(self,collection_name):
        self.docs = self.db.collection(collection_name).get()
        return self.docs


    def insert(self,collection_name,data):
        self.db.collection(collection_name).document().set(data)
    

    def update(self,collection_name,doc_id,data):
        self.db.collection(collection_name).document(doc_id).update(data)
        
    
    def validation_data(self,data):
        if data