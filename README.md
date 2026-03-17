# sfmc-ac-flask

**Salesforce Marketing Cloud (SFMC) Journey Builder** 向けカスタムアクティビティの Flask アプリケーション

Journey Builder のジャーニーフロー内でコンタクト情報を **Google Cloud Firestore** に登録し、DialogOne との連携を実現します。

---

## 目次

- [概要](#概要)
- [技術スタック](#技術スタック)
- [ディレクトリ構成](#ディレクトリ構成)
- [アプリケーション全体フロー](#アプリケーション全体フロー)
- [API リファレンス](#api-リファレンス)
- [モデル定義](#モデル定義)
- [フロントエンド仕様](#フロントエンド仕様)
- [config.json 仕様](#configjson-仕様)
- [セットアップ](#セットアップ)
- [デプロイ](#デプロイ)

---

## 概要

### 主な機能

- Journey Builder カスタムアクティビティとしての動作（設定UI + REST APIエンドポイント）
- ジャーニー実行時にコンタクト情報を Firestore へ保存
- DialogOne との連携を目的としたデータ受け渡し

### 連携先サービス

| サービス | 用途 |
|---|---|
| SFMC Journey Builder | カスタムアクティビティとして動作 |
| Google Cloud Firestore | ユーザーデータの永続化（コレクション: `smc_connect_users`）|
| Google Cloud Logging | アプリケーションログの送信 |
| DialogOne | SFMC データエクステンション `DONE_USERS` 経由でユーザー属性を取得 |

---

## 技術スタック

| カテゴリ | 技術 |
|---|---|
| バックエンド | Python 3 / Flask 3.0.0 |
| WSGI サーバー | Gunicorn 19.9.0 |
| データベース | Google Cloud Firestore |
| ロギング | Google Cloud Logging |
| フロントエンド | HTML / JavaScript / Semantic UI |
| JB連携ライブラリ | Postmonger.js 0.0.14 |
| コンテナ | Docker |
| デプロイ先 | Google Cloud Run |

### 依存パッケージ

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

## ディレクトリ構成

```
sfmc-ac-flask/
├── app.py                  # Flask メインアプリケーション
├── config.json             # SFMC カスタムアクティビティ定義ファイル
├── Dockerfile              # Docker コンテナビルド定義
├── Procfile                # Heroku / Cloud Run 用プロセス定義
├── requirements.txt        # Python 依存パッケージ一覧
├── README.md
├── models/
│   └── users.py            # Users モデル（Firestore データ操作）
├── static/
│   ├── css/
│   │   ├── main.css        # カスタムスタイル
│   │   ├── semantic.css    # Semantic UI
│   │   └── semantic.min.css
│   ├── img/
│   │   └── done.png        # アクティビティアイコン
│   └── js/
│       ├── index.js        # カスタムアクティビティ UI ロジック
│       ├── postmonger.js   # JB 通信ライブラリ
│       ├── semantic.js     # Semantic UI JS
│       └── semantic.min.js
├── templates/
│   └── index.html          # カスタムアクティビティ設定画面
└── docs/                   # 詳細ドキュメント
```

---

## アプリケーション全体フロー

```
┌─────────────────────────────────────────────────────────┐
│              SFMC Journey Builder                        │
│                                                         │
│   1. ジャーニーにカスタムアクティビティを配置            │
│   2. 設定画面 (index.html) で content_id を入力          │
│   3. ジャーニー実行時に /execute エンドポイントへPOST     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Flask アプリケーション (app.py)             │
│                                                         │
│   /execute (POST)                                       │
│     → inArguments からユーザーデータを取得               │
│     → Users モデルで Firestore へ保存                    │
│                                                         │
│   /save, /publish, /validate (POST)                     │
│     → JB ライフサイクルイベントの受信                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Google Cloud Firestore                      │
│                                                         │
│   コレクション: smc_connect_users                       │
│   フィールド: contact_key, uid, acid, campaign_id,       │
│              content_id, send_flg                        │
└─────────────────────────────────────────────────────────┘
```

### Journey Builder ライフサイクル

```
アクティビティ配置 → 設定画面表示 (/index.html)
    → /save (POST)     : 設定保存
    → /validate (POST) : バリデーション
    → /publish (POST)  : ジャーニー公開
    → /execute (POST)  : ジャーニー実行（各コンタクトに対して）
    → /stop (POST)     : ジャーニー停止 ※未実装
```

---

## API リファレンス

### エンドポイント一覧

| メソッド | パス | 用途 | カテゴリ |
|---|---|---|---|
| GET | `/` | 設定画面の表示 | UI |
| GET | `/index.html` | 設定画面の表示（別名） | UI |
| GET | `/config.json` | アクティビティ定義の取得 | JB連携 |
| POST | `/execute` | ジャーニー実行時の処理 | JB連携 |
| POST | `/publish` | ジャーニー公開時の処理 | JB連携 |
| POST | `/save` | アクティビティ保存時の処理 | JB連携 |
| POST | `/validate` | アクティビティ検証時の処理 | JB連携 |
| POST | `/dotest` | テスト用データ受信 | テスト |
| GET | `/storetest` | Firestore テストデータ挿入 | テスト |

### POST `/execute`

ジャーニー実行時に呼び出され、ユーザーデータを Firestore に保存します。

**リクエストボディ**:
```json
{
  "inArguments": [
    {
      "contact_key": "user@example.com",
      "uid": "12345",
      "acid": "50dbb3948b683b5a",
      "campaign_id": "campaign_001",
      "content_id": "39812"
    }
  ]
}
```

**inArguments フィールド**:

| フィールド | 型 | 説明 |
|---|---|---|
| `contact_key` | string | SFMC コンタクトキー（`{{Contact.Key}}`） |
| `uid` | string | ユーザーID（DE `DONE_USERS` の `UID`） |
| `acid` | string | ACID（DE `DONE_USERS` の `ACID`） |
| `campaign_id` | string | キャンペーンID（DE `DONE_USERS` の `campaign_id`） |
| `content_id` | string | コンテンツID（設定画面で入力された値） |

**処理内容**:
1. `inArguments[0]` を取得
2. `Users` モデルを生成し、Firestore コレクション `smc_connect_users` にドキュメント追加
3. `send_flg: false` が自動付与される

**レスポンス**: `200 OK`

### POST `/publish`・`/save`・`/validate`

JB ライフサイクルイベント受信用。ログ出力のみで追加処理なし。すべて `200 OK` を返します。

### POST `/dotest`

テスト用。JSONボディから `uid` を受け取りコンソール出力。

### GET `/storetest`

Firestore へ固定テストデータ挿入。

> **注意**: `/dotest`・`/storetest` は開発用であり、本番環境では無効化推奨。

---

## モデル定義

### Users クラス（`models/users.py`）

Firestore へのユーザーデータ登録を担当するモデルクラスです。

```python
class Users:
    def __init__(self, db, jdata)
    def insert(self, collection_name)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `db` | `firestore.Client` | Firestore クライアントインスタンス |
| `jdata` | `dict` | SFMC から受信した inArguments データ |

**保存されるフィールド**:

| フィールド | 型 | 説明 |
|---|---|---|
| `contact_key` | string | SFMC コンタクトキー |
| `uid` | string | ユーザーID |
| `acid` | string | ACID |
| `campaign_id` | string | キャンペーンID |
| `content_id` | string | コンテンツID |
| `send_flg` | boolean | 送信済みフラグ（初期値: `false`） |

**使用例**:
```python
users = Users(db, jdata)
users.insert("smc_connect_users")
```

> `send_flg` は初期値 `false` で挿入され、後続処理で `true` に更新される設計です。  
> バリデーションチェック（`validation_data`）は未実装です。

---

## フロントエンド仕様

### 設定画面（`templates/index.html`）

Journey Builder の iframe 内で表示される設定画面です。

| 要素 | 説明 |
|---|---|
| Content_id 入力フィールド | コンテンツIDを入力するテキストフィールド |
| Save ボタン | 設定を保存し JB に反映 |
| Cancel ボタン | 変更を破棄して画面を閉じる |

### JavaScript ロジック（`static/js/index.js`）

| 変数 | 値 | 説明 |
|---|---|---|
| `connection` | `Postmonger.Session` | JB との通信セッション |
| `activity` | `null` | アクティビティオブジェクト |
| `dataExtentionName` | `"DONE_USERS"` | 参照するデータエクステンション名 |

**イベントフロー**:
```
DOMContentLoaded
  ├── setupEventHandlers()           // ボタンイベント設定
  ├── connection.on('initActivity')  // 初期化イベントバインド
  └── connection.trigger('ready')    // JB に準備完了通知
        ↓
  onInitActivity(payload)            // JB からアクティビティ情報受信
```

**Save ボタン（`onDoneButtonClick`）の処理**:
1. `isConfigured = true` を設定
2. 入力された `content_id` を取得
3. `inArguments` を構築（SFMC パーソナライゼーション文字列でDE参照）
4. `updateActivity` で JB に通知

**参照するSFMCパーソナライゼーション文字列**:

| 文字列 | 参照先 |
|---|---|
| `{{Contact.Key}}` | コンタクトキー |
| `{{Contact.Attribute.DONE_USERS.UID}}` | ユーザーID |
| `{{Contact.Attribute.DONE_USERS.ACID}}` | ACID |
| `{{Contact.Attribute.DONE_USERS.name}}` | 名前 |
| `{{Contact.Attribute.DONE_USERS.campaign_id}}` | キャンペーンID |

> `dataExtentionName` を変更することで参照先DEを切り替え可能。

---

## config.json 仕様

SFMC Journey Builder がカスタムアクティビティを認識・制御するための定義ファイルです。

### 主要プロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| `workflowApiVersion` | `"1.1"` | JB Workflow API バージョン |
| `type` | `"REST"` | アクティビティタイプ |
| `metaData.icon` | `/static/img/done.png` | アイコン画像パス |
| `metaData.category` | `"message"` | カテゴリ |
| `lang.en-US.name` | `"DialogOne"` | 表示名 |

### arguments.execute

| プロパティ | 値 | 説明 |
|---|---|---|
| `timeout` | `20000` | タイムアウト（20秒） |
| `retryCount` | `1` | リトライ回数 |
| `retryDelay` | `10000` | リトライ間隔（10秒） |
| `concurrentRequests` | `1` | 同時リクエスト数 |

### configurationArguments

| イベント | パス | 説明 |
|---|---|---|
| `save` | `/save` | 設定保存時 |
| `publish` | `/publish` | ジャーニー公開時 |
| `validate` | `/validate` | バリデーション時 |
| `stop` | `/stop` | ジャーニー停止時（**※未実装**）|

### configModal

| プロパティ | 値 |
|---|---|
| `height` | 200 |
| `width` | 300 |
| `fullscreen` | true |

---

## セットアップ

### 前提条件

- Python 3.x
- Google Cloud プロジェクト（Firestore、Cloud Logging が有効化済み）
- Google Cloud SDK（ローカル開発時）
- Docker（コンテナビルド時）
- SFMC 管理者権限（カスタムアクティビティの登録）

### 1. 環境構築

```bash
python3 -m venv venv
source venv/bin/activate
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

`http://0.0.0.0:8080` で起動します。

---

## デプロイ

### Docker

```bash
docker build -t sfmc-ac-flask .
docker run -p 8080:8080 sfmc-ac-flask
```

### Google Cloud Run

```bash
export PROJECT_ID=your-gcp-project-id

# ビルド & プッシュ
gcloud builds submit --tag gcr.io/$PROJECT_ID/sfmc-ac-flask

# デプロイ
gcloud run deploy sfmc-ac-flask \
  --image gcr.io/$PROJECT_ID/sfmc-ac-flask \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

デプロイ後、取得した Cloud Run の URL を `config.json` の以下に反映：
- `arguments.execute.url`
- `configurationArguments.save.url`
- `configurationArguments.publish.url`
- `configurationArguments.validate.url`
- `configurationArguments.stop.url`

### Heroku

```bash
heroku create sfmc-ac-flask
git push heroku main
```

### SFMC への登録

1. SFMC **Package Manager** でアプリケーションパッケージを作成
2. **Journey Builder Activity** コンポーネントを追加
3. エンドポイント URL にデプロイ先の URL を設定
4. `config.json` の URL が正しいことを確認

---

## ドキュメント

詳細なドキュメントは [`docs/`](docs/) ディレクトリを参照してください：

- [プロジェクト概要](docs/overview.md)
- [API リファレンス](docs/api-reference.md)
- [モデル定義](docs/models.md)
- [フロントエンド仕様](docs/frontend.md)
- [config.json 仕様書](docs/config-json-spec.md)
- [セットアップ・デプロイガイド](docs/setup-and-deployment.md)

PDF版: [`docs/sfmc-ac-flask-documentation.pdf`](docs/sfmc-ac-flask-documentation.pdf)