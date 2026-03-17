# セットアップ・デプロイガイド

## 前提条件

- Python 3.x
- Google Cloud プロジェクト（Firestore、Cloud Logging が有効化済み）
- Google Cloud SDK（ローカル開発時）
- Docker（コンテナビルド時）
- SFMC 管理者権限（カスタムアクティビティの登録）

---

## 依存パッケージ

`requirements.txt` に定義されたパッケージ一覧：

| パッケージ | バージョン | 用途 |
|---|---|---|
| flask | 3.0.0 | Web フレームワーク |
| gunicorn | 19.9.0 | WSGI HTTP サーバー |
| requests | 2.31.0 | HTTP クライアント |
| firebase-admin | 6.2.0 | Firebase Admin SDK |
| google-cloud-firestore | 2.13.0 | Firestore クライアント |
| google-cloud-logging | 3.8.0 | Cloud Logging クライアント |
| PyYAML | 6.0.1 | YAML パーサー |

---

## ローカル開発

### 1. 環境構築

```bash
# 仮想環境の作成・有効化
python3 -m venv venv
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 2. Google Cloud 認証

```bash
# サービスアカウントキーを使用する場合
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"

# gcloud CLI でログインする場合
gcloud auth application-default login
```

### 3. アプリケーション起動

```bash
python app.py
```

アプリケーションは `http://0.0.0.0:8080` で起動します。

---

## Docker ビルド・実行

### Dockerfile の構成

```dockerfile
FROM python:3          # Python 3 ベースイメージ
USER root              # root ユーザーで実行

EXPOSE 8080:8080       # ポート 8080 を公開

# システム・pip の更新
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# 依存パッケージのインストール
COPY "./requirements.txt" /tmp
RUN pip install -r /tmp/requirements.txt

# アプリケーションコードのコピー
COPY ./. /app/
WORKDIR "/app"
CMD ["python","app.py"]
```

### ビルドと実行

```bash
# イメージのビルド
docker build -t sfmc-ac-flask .

# コンテナの実行
docker run -p 8080:8080 sfmc-ac-flask
```

---

## Google Cloud Run へのデプロイ

### 1. Container Registry / Artifact Registry へのプッシュ

```bash
# プロジェクトIDを設定
export PROJECT_ID=your-gcp-project-id

# イメージのビルドとプッシュ
gcloud builds submit --tag gcr.io/$PROJECT_ID/sfmc-ac-flask

# または Artifact Registry を使用
gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/repo-name/sfmc-ac-flask
```

### 2. Cloud Run へのデプロイ

```bash
gcloud run deploy sfmc-ac-flask \
  --image gcr.io/$PROJECT_ID/sfmc-ac-flask \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### 3. デプロイ後の設定

デプロイ後に取得した Cloud Run の URL を `config.json` の各エンドポイントURLに反映してください。

現在の設定値:
```
https://sfmc-done-test-akb3xrrmgq-uc.a.run.app
```

変更が必要な箇所（`config.json`）:
- `arguments.execute.url`
- `configurationArguments.save.url`
- `configurationArguments.publish.url`
- `configurationArguments.validate.url`
- `configurationArguments.stop.url`

---

## Heroku デプロイ（Procfile）

`Procfile` が定義されているため、Heroku へのデプロイも可能です。

```
web: gunicorn app:app --log-file ./log.txt
```

```bash
heroku create sfmc-ac-flask
git push heroku main
```

---

## SFMC への登録

カスタムアクティビティを SFMC に登録するには、以下の手順が必要です：

1. SFMC の **Package Manager** でアプリケーションパッケージを作成
2. **Journey Builder Activity** コンポーネントを追加
3. エンドポイント URL にデプロイ先の URL を設定
4. `config.json` のURLが正しくデプロイ先を指していることを確認

---

## 環境変数

現在のアプリケーションでは明示的な環境変数は使用されていませんが、以下の暗黙の設定が必要です：

| 設定 | 説明 |
|---|---|
| Google Cloud 認証情報 | Firestore・Cloud Logging アクセスに必要。Cloud Run では自動的にサービスアカウントが適用される |
| Firestore データベース | デフォルトの Firestore データベースを使用 |
