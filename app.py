from flask import *
import logging
import requests
import json

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
    
    ## 受け取ったデータをD1へ送信
    # connect_done(request.json)
    url = "https://http-receiver.onrender.com/"
    data = {
        "contact_key": request.json['inArguments'][0]['contact_key'],
        "uid":request.json['inArguments'][0]['uid'],
        "acid":request.json['inArguments'][0]['acid'],
        "creative_id":request.json['inArguments'][0]['creative_id']
            }
    print("data:",data)
    
    headers = {'content-type': 'application/json'}
    res = requests.post(url,data=json.dumps(data),headers=headers)
    print(res.status_code)
    if res.status_code==200:
        print("send success",res.txt)
    
    return make_response('Success', 200)

@app.route("/publish",methods=["post"])
def publish():
    print("publish")
    return make_response('Success', 200)

@app.route("/save",methods=["post"])
def save():
    print("save")
    return render_template("index.html")

@app.route("/validate",methods=["post"])
def validate():
    print("validate")
    return make_response('Success', 200)

@app.route("/dotest",methods=["post"])
def dpost():
    print("rceive")
    uid = request.json["uid"]
    
    print("---receive_data---:",uid)
    return make_response('Success', 200)

# アプリケーションを実行
if __name__ == '__main__':
    app.run()
