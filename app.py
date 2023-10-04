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
    connect_done(request.json)
    
    return jsonify({'message': 'hello internal'}), 200


def connect_done(data):
    url = "https://sfmc-ac-flask.onrender.com/d1endpoint_test"
    requests.post(url,data=data)

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

@app.route("/d1endpoint_test",methods=["post"])
def d1post():
    print("---receive_data----")
    print(request.json['inArguments'][0]['uid'])
    
    return make_response('Success', 200)

# アプリケーションを実行
if __name__ == '__main__':
    app.run()
