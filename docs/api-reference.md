# API リファレンス

本ドキュメントでは、Flask アプリケーションが提供する全 REST API エンドポイントについて記載します。

---

## エンドポイント一覧

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

---

## エンドポイント詳細

### GET `/`・`/index.html`

**概要**: Journey Builder のカスタムアクティビティ設定画面を返します。

**レスポンス**: `templates/index.html` をレンダリングした HTML

**説明**:  
Journey Builder でアクティビティを選択した際に表示される設定モーダル画面です。ユーザーは `content_id`（コンテンツID）を入力できます。

---

### GET `/config.json`

**概要**: SFMC カスタムアクティビティの定義ファイルを返します。

**レスポンス**: JSON（`config.json` の内容）

**レスポンス例**:
```json
{
  "workflowApiVersion": "1.1",
  "metaData": {
    "icon": "/static/img/done.png",
    "category": "message"
  },
  "type": "REST",
  "lang": {
    "en-US": {
      "name": "DialogOne",
      "description": "Connet to DialogOne"
    }
  },
  "arguments": {
    "execute": {
      "inArguments": [],
      "outArguments": [],
      "timeout": 20000,
      "retryCount": 1,
      "retryDelay": 10000,
      "concurrentRequests": 1,
      "url": "https://sfmc-done-test-akb3xrrmgq-uc.a.run.app/execute"
    }
  },
  "configurationArguments": {
    "save": { "url": "..." },
    "publish": { "url": "..." },
    "validate": { "url": "..." },
    "stop": { "url": "..." }
  },
  "userInterfaces": {
    "configModal": {
      "height": 200,
      "width": 300,
      "fullscreen": true
    }
  }
}
```

**主要フィールド説明**:

| フィールド | 説明 |
|---|---|
| `workflowApiVersion` | JB Workflow API のバージョン（1.1） |
| `metaData.icon` | アクティビティのアイコン画像パス |
| `metaData.category` | アクティビティのカテゴリ（`message`） |
| `type` | アクティビティタイプ（`REST`） |
| `arguments.execute` | ジャーニー実行時の設定（URL、タイムアウト、リトライ等） |
| `configurationArguments` | 各ライフサイクルイベント（save/publish/validate/stop）のURL |
| `userInterfaces.configModal` | 設定モーダルのサイズ設定 |

---

### POST `/execute`

**概要**: ジャーニー実行時に呼び出され、ユーザーデータを Firestore に保存します。

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
| `uid` | string | ユーザーID（データエクステンション `DONE_USERS` の `UID`） |
| `acid` | string | ACID（データエクステンション `DONE_USERS` の `ACID`） |
| `campaign_id` | string | キャンペーンID（データエクステンション `DONE_USERS` の `campaign_id`） |
| `content_id` | string | コンテンツID（設定画面で入力された値） |

**レスポンス**: `200 OK`（`Success`）

**処理内容**:
1. リクエストボディから `inArguments[0]` を取得
2. `Users` モデルを生成し、Firestore コレクション `smc_connect_users` にドキュメントを追加
3. 保存されるデータには `send_flg: false` が自動付与される

---

### POST `/publish`

**概要**: ジャーニーが公開（アクティベート）された際に呼び出されます。

**レスポンス**: `200 OK`（`Success`）

**処理内容**: ログ出力のみ。追加の処理は実装されていません。

---

### POST `/save`

**概要**: アクティビティの設定が保存された際に呼び出されます。

**レスポンス**: `index.html` テンプレートのレンダリング結果

**処理内容**: ログ出力のみ。

---

### POST `/validate`

**概要**: ジャーニー公開前のバリデーション時に呼び出されます。

**レスポンス**: `200 OK`（`Success`）

**処理内容**: ログ出力のみ。常に成功を返します。

---

### POST `/dotest`

**概要**: テスト用エンドポイント。JSON ボディから `uid` を受け取り、コンソールに出力します。

**リクエストボディ**:
```json
{
  "uid": "12345"
}
```

**レスポンス**: `200 OK`（`Success`）

---

### GET `/storetest`

**概要**: Firestore へテストデータを挿入するためのエンドポイントです。

**レスポンス**: `200 OK`（`Success`）

**処理内容**: `test_collection` コレクションに以下の固定データを挿入します。

```json
{
  "contact_key": "ryo-tsubota@dac.co.jp",
  "uid": "1212",
  "acid": "50dbb3948b683b5a",
  "content_id": "39812",
  "send_flg": false
}
```

> **注意**: このエンドポイントは開発・テスト目的のものであり、本番環境では無効化することを推奨します。
