from flask import *
import logging
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from models.users import Users

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)
logger = logging.getLogger('weblog')
logger.setLevel(logging.DEBUG)

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

@app.route("/execute",methods=["GET", "POST"])
def execute():

    logger.debug("execute")
    logger.debug(request.json)
    
    ## 受け取ったデータをFireStoreへ登録

    data = {
        "contact_key": request.json['inArguments'][0]['contact_key'],
        "uid":request.json['inArguments'][0]['uid'],
        "acid":request.json['inArguments'][0]['acid'],
        "creative_id":request.json['inArguments'][0]['creative_id'],
        "send_flg": False
        }
    logger.debug("data:",data)
    
    user = Users(data)
    
    try:
        user.insert("smc_connect_users")
        logger.info("db connected")
        return make_response('Success', 200)
    except:
        logger.error("db connection error")
        return make_response('Error', 400)
        
@app.route("/publish",methods=["POST"])
def publish():
    logger.debug("publish")
    return make_response('Success', 200)

@app.route("/save",methods=["POST"])
def save():
    logger.debug("save")
    return render_template("index.html")

@app.route("/validate",methods=["POST"])
def validate():
    logger.debug("validate")
    return make_response('Success', 200)

@app.route("/dotest",methods=["POST"])
def dpost():
    logger.debug("rceive")
    uid = request.json["uid"]
    
    print("---receive_data---:",uid)
    return make_response('Success', 200)


# アプリケーションを実行
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)
