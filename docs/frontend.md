# フロントエンド仕様

## 概要

カスタムアクティビティの設定画面（UI）は、Journey Builder の iframe 内で表示されます。  
Postmonger.js を使用して Journey Builder 本体と通信し、アクティビティの設定情報をやり取りします。

---

## 設定画面（index.html）

### 画面構成

| 要素 | 説明 |
|---|---|
| Content_id 入力フィールド | コンテンツIDをユーザーが入力するテキストフィールド |
| Save ボタン | 設定を保存し、Journey Builder に反映する |
| Cancel ボタン | 変更を破棄して設定画面を閉じる |

### 使用ライブラリ

| ライブラリ | バージョン | 用途 |
|---|---|---|
| jQuery | 3.7.1 (slim) | DOM操作 |
| Semantic UI | - | UIフレームワーク（フォーム、ボタン等） |
| Postmonger.js | 0.0.14 | Journey Builder との通信 |

### スタイル（main.css）

| クラス | 説明 |
|---|---|
| `.container` | 最大幅960px、中央揃えのメインコンテナ |
| `.btn_group` | ボタングループ（上マージン30px） |
| `.topmargin` | 上マージン30px |
| `.center` | テキスト中央揃え |

---

## JavaScript ロジック（index.js）

### 定数

| 変数 | 値 | 説明 |
|---|---|---|
| `connection` | `Postmonger.Session` | JB との通信セッション |
| `activity` | `null`（初期値） | アクティビティオブジェクト |
| `dataExtentionName` | `"DONE_USERS"` | 参照するデータエクステンション名 |

### イベントフロー

```
DOMContentLoaded
    │
    ├── setupEventHandlers()   // ボタンイベントの設定
    ├── connection.on('initActivity', onInitActivity)   // 初期化イベントのバインド
    └── connection.trigger('ready')   // JB に準備完了を通知
          │
          ▼
    onInitActivity(payload)
          │  ← JB からアクティビティオブジェクトを受信
          └── activity 変数にペイロードを保存
```

### 関数詳細

#### `onInitActivity(payload)`

Journey Builder から受信したアクティビティ情報を処理します。

- `activity` 変数にペイロードを格納
- `inArguments` の有無を確認
- デバッグ用にコンソールへ情報を出力

#### `onDoneButtonClick()`

Save ボタンクリック時の処理です。

**処理フロー**:
1. `activity.metaData.isConfigured = true` を設定（アクティビティが設定済みであることをJBに通知）
2. 入力された `content_id` を取得
3. `inArguments` を構築:

```javascript
activity.arguments.execute.inArguments = [{
    content_id: content_id,                              // 画面入力値
    contact_key: "{{Contact.Key}}",                      // SFMC コンタクトキー
    uid: "{{Contact.Attribute.DONE_USERS.UID}}",         // データエクステンション参照
    acid: "{{Contact.Attribute.DONE_USERS.ACID}}",       // データエクステンション参照
    name: "{{Contact.Attribute.DONE_USERS.name}}",       // データエクステンション参照
    campaign_id: "{{Contact.Attribute.DONE_USERS.campaign_id}}" // データエクステンション参照
}];
```

4. アクティビティ名を `content_id` の値に設定
5. `connection.trigger('updateActivity', activity)` で JB にアクティビティ更新を通知

#### `onCancelButtonClick()`

Cancel ボタンクリック時の処理です。

1. `setActivityDirtyState` を `false` に設定（変更なし扱い）
2. `requestInspectorClose` でインスペクター（設定画面）を閉じる

### SFMC データエクステンション参照

フロントエンドでは、SFMC のパーソナライゼーション文字列を使用してデータエクステンション `DONE_USERS` から以下の属性を参照しています：

| パーソナライゼーション文字列 | 参照先 |
|---|---|
| `{{Contact.Key}}` | コンタクトキー |
| `{{Contact.Attribute.DONE_USERS.UID}}` | ユーザーID |
| `{{Contact.Attribute.DONE_USERS.ACID}}` | ACID |
| `{{Contact.Attribute.DONE_USERS.name}}` | 名前 |
| `{{Contact.Attribute.DONE_USERS.campaign_id}}` | キャンペーンID |

> **注意**: `dataExtentionName` 変数（`"DONE_USERS"`）を変更することで、参照先のデータエクステンションを切り替えられます。コード内に `TODO: データエクステンション名に応じ変更する` のコメントがあります。
