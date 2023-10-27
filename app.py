from flask import *
import logging
import google.cloud.logging
import requests
import json
from firebase_admin import firestore
from models.users import Users
import yaml

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
    with open('./fileconfig.yaml') as file:
        global config
        config = yaml.safe_load(file)
    logger.info("--execute--")
    
    ## 受け取ったデータをFireStoreへ登録
    jdata = request.json['inArguments'][0]
    logger.debug(f"jdata:{jdata}")
    users = Users(db, jdata)
    try:
        logger.debug(config["collection_name"])
    except Exception as e:
        logger.debug(e)
    users.insert("smc_connect_users")
    logger.info("--insert end--")
    
    return make_response('Success', 200)

            
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
    db.collection("test_collection").document().set({'contact_key': 'ryo-tsubota@dac.co.jp', 'uid': '1212', 'acid': '50dbb3948b683b5a', 'content_id': '39812', 'send_flg': False})
    logger.debug("testdata insert")
    
    
    return make_response('Success', 200)

# アプリケーションを実行
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
