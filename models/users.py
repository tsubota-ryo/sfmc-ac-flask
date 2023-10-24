import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class Users():
    
    def __init__(self,data):
        print("init start")
        self.db = firestore.Client()
        print("create db")
        
        self.data = data
        print("init end")
        
    def get_documents(self,collection_name):
        self.docs = self.db.collection(collection_name).get()
        return self.docs


    def insert(self,collection_name):
        print(collection_name)
        self.db.collection(collection_name).document().set(self.data)
    

    def update(self,collection_name,doc_id):
        self.db.collection(collection_name).document(doc_id).update(self.data)
        
    # TODO:validation check
    # def validation_data(self,data):
    #     if data