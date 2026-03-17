# config.json 仕様書

## 概要

`config.json` は、SFMC Journey Builder がカスタムアクティビティを認識・制御するための**アクティビティ定義ファイル**です。  
Journey Builder はこのファイルを読み込み、アクティビティの表示名、アイコン、各ライフサイクルイベントのエンドポイントURL等を取得します。

---

## 構造

### トップレベルプロパティ

| プロパティ | 値 | 説明 |
|---|---|---|
| `workflowApiVersion` | `"1.1"` | Journey Builder Workflow API のバージョン |
| `type` | `"REST"` | アクティビティタイプ（REST API ベース） |

### metaData

アクティビティのメタ情報を定義します。

| プロパティ | 値 | 説明 |
|---|---|---|
| `icon` | `"/static/img/done.png"` | JB キャンバス上に表示されるアイコン画像のパス |
| `category` | `"message"` | アクティビティのカテゴリ（JB のパレットでの表示位置） |

### lang

アクティビティの多言語表示設定です。

| ロケール | name | description |
|---|---|---|
| `en-US` | DialogOne | Connet to DialogOne |

### arguments.execute

ジャーニー実行時の設定です。

| プロパティ | 値 | 説明 |
|---|---|---|
| `inArguments` | `[]` | 実行時に渡される引数（フロントエンドで動的に設定） |
| `outArguments` | `[]` | 実行後に返される引数（未使用） |
| `timeout` | `20000` | タイムアウト（ミリ秒）：20秒 |
| `retryCount` | `1` | リトライ回数 |
| `retryDelay` | `10000` | リトライ間隔（ミリ秒）：10秒 |
| `concurrentRequests` | `1` | 同時リクエスト数 |
| `url` | `"https://sfmc-done-test-akb3xrrmgq-uc.a.run.app/execute"` | 実行エンドポイントURL |

### configurationArguments

各ライフサイクルイベントのエンドポイントURLです。

| イベント | パス | 説明 |
|---|---|---|
| `save` | `/save` | アクティビティ設定の保存時 |
| `publish` | `/publish` | ジャーニーのアクティベート時 |
| `validate` | `/validate` | ジャーニー公開前のバリデーション時 |
| `stop` | `/stop` | ジャーニー停止時（※エンドポイント未実装） |

> **注意**: `/stop` エンドポイントは `config.json` で定義されていますが、`app.py` には対応するルートが実装されていません。

### userInterfaces.configModal

アクティビティ設定画面のモーダル設定です。

| プロパティ | 値 | 説明 |
|---|---|---|
| `height` | `200` | モーダルの高さ（px） |
| `width` | `300` | モーダルの幅（px） |
| `fullscreen` | `true` | フルスクリーン表示（`true` の場合、width/height は無視される） |

---

## Journey Builder ライフサイクル

```
アクティビティ配置
    │
    ▼
設定画面表示 (/index.html)
    │
    ▼ ユーザーが設定を保存
/save (POST)
    │
    ▼ ジャーニーを公開
/validate (POST) → /publish (POST)
    │
    ▼ ジャーニー実行（各コンタクトに対して）
/execute (POST)
    │
    ▼ ジャーニー停止
/stop (POST)  ※未実装
```
