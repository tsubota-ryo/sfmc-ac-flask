# SFMC Custom Activity - Flask アプリケーション概要

## 1. プロジェクト概要

本プロジェクトは、**Salesforce Marketing Cloud (SFMC) Journey Builder** 向けのカスタムアクティビティを提供するWebアプリケーションです。  
Flask（Python）をバックエンドとして使用し、Journey Builder のジャーニーフロー内でユーザー情報を **Google Cloud Firestore** に登録する機能を実現しています。

### 主な機能

- Journey Builder カスタムアクティビティとしての動作（設定UI + REST APIエンドポイント）
- ジャーニー実行時にコンタクト情報を Firestore へ保存
- DialogOne との連携を目的としたデータ受け渡し

### 技術スタック

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

---

## 2. ディレクトリ構成

```
sfmc-ac-flask/
├── app.py                  # Flask メインアプリケーション
├── config.json             # SFMC カスタムアクティビティ定義ファイル
├── Dockerfile              # Docker コンテナビルド定義
├── Procfile                # Heroku / Cloud Run 用プロセス定義
├── requirements.txt        # Python 依存パッケージ一覧
├── README.md               # プロジェクト概要（簡易）
├── models/
│   └── users.py            # Users モデル（Firestore データ操作）
├── static/
│   ├── css/
│   │   ├── main.css        # カスタムスタイル
│   │   ├── semantic.css    # Semantic UI（フル版）
│   │   └── semantic.min.css # Semantic UI（圧縮版）
│   ├── img/
│   │   └── done.png        # アクティビティアイコン（推定）
│   └── js/
│       ├── index.js        # カスタムアクティビティ UI ロジック
│       ├── postmonger.js   # JB 通信ライブラリ
│       ├── semantic.js     # Semantic UI JS（フル版）
│       └── semantic.min.js # Semantic UI JS（圧縮版）
├── templates/
│   └── index.html          # カスタムアクティビティ設定画面テンプレート
└── docs/                   # ドキュメント（本ディレクトリ）
```

---

## 3. アプリケーションの全体フロー

```
┌─────────────────────────────────────────────────────────┐
│              SFMC Journey Builder                        │
│                                                         │
│   1. ジャーニーにカスタムアクティビティを配置            │
│   2. 設定画面 (index.html) で content_id を入力          │
│   3. ジャーニー実行時に /execute エンドポイントへPOST     │
│                                                         │
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
│                                                         │
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

---

## 4. 連携先サービス

### Salesforce Marketing Cloud (SFMC)
- Journey Builder のカスタムアクティビティとして動作
- `config.json` で定義されたエンドポイントURLを通じてJBと通信

### Google Cloud Firestore
- ジャーニー実行時のユーザーデータを永続化
- コレクション名: `smc_connect_users`

### Google Cloud Logging
- アプリケーションログをCloud Loggingへ送信
- ログレベル: DEBUG

### DialogOne
- `config.json` の `lang` 設定で "DialogOne" と記載
- SFMC のデータエクステンション `DONE_USERS` を参照してユーザー属性を取得
