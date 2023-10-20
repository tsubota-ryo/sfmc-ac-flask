from flask import *
import logging
import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import models.users

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

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
    print("execute")
    print(request.json)
    
    ## 受け取ったデータをFireStoreへ登録
    # connect_done(request.json)
    # url = "https://http-receiver.onrender.com/"
    data = {
        "contact_key": request.json['inArguments'][0]['contact_key'],
        "uid":request.json['inArguments'][0]['uid'],
        "acid":request.json['inArguments'][0]['acid'],
        "creative_id":request.json['inArguments'][0]['creative_id']
            }
    print("data:",data)
    
    user = Users(data)
    
    try:
        user.insert("smc_connect_users")
        return make_response('Success', 200)
    except:
        print("error")
        return make_response('Error', 400)
        
    
    # headers = {'content-type': 'application/json'}
    # res = requests.post(url,data=json.dumps(data),headers=headers)
    # print(res.status_code)
    # if res.status_code==200:
    #     print("send success",res.txt)
    
    

@app.route("/publish",methods=["POST"])
def publish():
    print("publish")
    return make_response('Success', 200)

@app.route("/save",methods=["POST"])
def save():
    print("save")
    return render_template("index.html")

@app.route("/validate",methods=["POST"])
def validate():
    print("validate")
    return make_response('Success', 200)

@app.route("/dotest",methods=["POST"])
def dpost():
    print("rceive")
    uid = request.json["uid"]
    
    print("---receive_data---:",uid)
    return make_response('Success', 200)

@app.route("/fstest",method=["GET"])
def fstest():
    db = firestore.Client()
    db.collection("test_collection").document().set({"test":1})
    
    
    return make_response('Success', 200)
    

# アプリケーションを実行
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)
