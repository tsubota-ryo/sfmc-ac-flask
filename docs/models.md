# モデル定義

## Users モデル

**ファイル**: `models/users.py`

### 概要

Firestore へのユーザーデータ登録を担当するモデルクラスです。  
SFMC Journey Builder の `/execute` エンドポイントから呼び出され、ジャーニー実行時のコンタクト情報を永続化します。

### クラス定義

```python
class Users:
    def __init__(self, db, jdata)
    def insert(self, collection_name)
```

### コンストラクタ

```python
def __init__(self, db, jdata)
```

| 引数 | 型 | 説明 |
|---|---|---|
| `db` | `firestore.Client` | Firestore クライアントインスタンス |
| `jdata` | `dict` | SFMC から受信した inArguments データ |

コンストラクタでは、受信データから以下のフィールドを抽出して `self.data` に格納します：

| フィールド | 説明 | ソース |
|---|---|---|
| `contact_key` | SFMC コンタクトキー | `jdata['contact_key']` |
| `uid` | ユーザーID | `jdata['uid']` |
| `acid` | ACID | `jdata['acid']` |
| `campaign_id` | キャンペーンID | `jdata['campaign_id']` |
| `content_id` | コンテンツID | `jdata['content_id']` |
| `send_flg` | 送信フラグ（初期値: `False`） | 固定値 |

### メソッド

#### `insert(collection_name)`

Firestore の指定コレクションにドキュメントを追加します。

| 引数 | 型 | 説明 |
|---|---|---|
| `collection_name` | `str` | 保存先の Firestore コレクション名 |

**使用例**（`app.py` 内）:
```python
users = Users(db, jdata)
users.insert("smc_connect_users")
```

**例外処理**: Firestore への書き込みに失敗した場合、エラーをログ出力した後に例外を再送出します。

### Firestore データ構造

**コレクション名**: `smc_connect_users`

| フィールド | 型 | 説明 |
|---|---|---|
| `contact_key` | string | SFMC コンタクトキー（メールアドレス等） |
| `uid` | string | ユーザーID |
| `acid` | string | ACID |
| `campaign_id` | string | キャンペーンID |
| `content_id` | string | コンテンツID |
| `send_flg` | boolean | 送信済みフラグ（初期値: `false`） |

> **備考**: `send_flg` は初期値 `false` で挿入され、後続の処理（外部システム等）で `true` に更新される設計と推定されます。

### 未実装機能

- バリデーションチェック（`validation_data` メソッド）がコメントアウトされており、未実装の状態です。
