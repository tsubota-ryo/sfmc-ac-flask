from flask import *
import logging
import google.cloud.logging
import requests
import json
from firebase_admin import firestore
from models.users import Users

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

logger = logging.getLogger('weblog')
logger.setLevel(logging.DEBUG)
client = google.cloud.logging.Client()
client.setup_logging()


global db
db = firestore.Client()

# ルートURL ("/") へのアクセス時の処理
@app.route("/")
@app.route('/index.html')
def root():
    return render_template("index.html")

@app.route('/config.json')
def config():
    with open('./config.json') as f:
        jdata = json.load(f)
    return jsonify(jdata)

@app.route("/execute",methods=["POST"])
def execute():

    logger.info("--execute--")
    ## 受け取ったデータをFireStoreへ登録
    data = {
        "contact_key": request.json['inArguments'][0]['contact_key'],
        "uid":request.json['inArguments'][0]['uid'],
        "acid":request.json['inArguments'][0]['acid'],
        "content_id":request.json['inArguments'][0]['content_id'],
        "send_flg": False
        }
    logger.debug(f"data:{data}")

    db.collection("smc_connect_users").document().set(data)
    logger.info("--insert end--")
    return make_response('Success', 200)
    # try:
    #     logger.info("--insert start--")
    #     logger.info(db)
    #     # db.collection("smc_connect_users").document().set(data)
    #     db.collection("test_collection").document().set({"data":"test","send_flg":False})
    #     logger.info("--insert end--")
    #     # user = Users(data,db)       
    #     # user.insert(db,"smc_connect_users")
        
    #     return make_response('Success', 200)
    
    # except Exception as e:
    #     logger.error(f"db connection error:{e}")
        
    #     return make_response('Error', 400)
            
@app.route("/publish",methods=["POST"])
def publish():
    logger.debug("--publish--")
    return make_response('Success', 200)

@app.route("/save",methods=["POST"])
def save():
    logger.debug("--save--")
    return render_template("index.html")

@app.route("/validate",methods=["POST"])
def validate():
    logger.debug("--validate--")
    return make_response('Success', 200)

@app.route("/dotest",methods=["POST"])
def dpost():
    logger.debug("--receive--")
    uid = request.json["uid"]
    
    print("---receive_data---:",uid)
    return make_response('Success', 200)

@app.route("/storetest",methods=["GET"])
def storetest():
    db = firestore.Client()
    db.collection("test_collection").document().set({"data":"test","send_flg":False})
    logger.debug("testdata insert")
    
    
    return make_response('Success', 200)

# アプリケーションを実行
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
