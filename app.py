from flask import Flask

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# ルートURL ("/") へのアクセス時の処理
@app.route('/')
def hello_world():
    return 'Hello, World!'

# アプリケーションを実行
if __name__ == '__main__':
    app.run()
