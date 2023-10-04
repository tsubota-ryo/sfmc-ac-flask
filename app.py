from flask import *
import logging
import requests

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
    url = "https://sfmc-ac-flask.onrender.com//dotest"
    data = {"uid":request.json['inArguments'][0]['uid']}
    print("data:",data)
    res = requests.post(url,data=data)
    
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
