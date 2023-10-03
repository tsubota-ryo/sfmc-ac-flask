from flask import *
import logging

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# ルートURL ("/") へのアクセス時の処理
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
    return request.get_json()

# アプリケーションを実行
if __name__ == '__main__':
    app.run()
