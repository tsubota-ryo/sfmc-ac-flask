from flask import *
import logging

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
    print(request.method)
    return jsonify({'message': 'hello internal'}), 200

@app.route("/publish",methods=["post"])
def publish():
    print("publish")
    return render_template("index.html")

@app.route("/save",methods=["post"])
def save():
    print("save")
    return render_template("index.html")


# アプリケーションを実行
if __name__ == '__main__':
    app.run()
