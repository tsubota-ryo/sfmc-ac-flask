from flask import *

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# ルートURL ("/") へのアクセス時の処理
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/config.json')
def config():
    with open('./config.json') as f:
        jdata = json.load(f)
    return jsonify(jdata)

# アプリケーションを実行
if __name__ == '__main__':
    app.run()
