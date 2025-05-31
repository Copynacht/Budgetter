
# Budgetter 家計簿アプリ

このプロジェクトは家計簿アプリ「Budgetter」のDocker構成をまとめたものです。  
Docker Composeを利用して以下のサービスを一括で起動できます。

---

## サービス構成

- **budgetter-db**: MySQLデータベースコンテナ (mysql:9.3.0)
- **budgetter-api**: バックエンドAPI (Djangoなど想定)
- **budgetter-front**: フロントエンド (Nuxt.js)
- **budgetter-nginx**: リバースプロキシ・静的ファイル配信用のNginx

---

## 前提

- `.env`および`.env.budgetter-api`ファイルは`setup.sh`スクリプトにより自動作成されます。  
  生成されたファイルを編集してください。  
- DockerおよびDocker Composeがインストールされていること。

---

## 1. 初期セットアップ

まずは`setup.sh`を実行して環境変数ファイルを生成してください。

```bash
./setup.sh
```

---

## 2. Docker Composeで起動

```bash
docker compose up -d
```

- 各サービスがバックグラウンドで起動します。
- MySQLの初期化やAPIの起動は健康チェックによって制御されます。

---

## 3. サービス詳細

### budgetter-db

- MySQL 9.3.0イメージを使用。
- ポート3307でホストと接続可能。
- ボリューム`budgetter_mysql_data`にデータを永続化。
- 環境変数は`.env`および`.env.budgetter-api`で設定される。

### budgetter-api

- Django等のバックエンドAPIを想定。
- `/vol/www/static/budgetter`ディレクトリをマウントし静的ファイルを配信。
- `apache.conf`を設定として利用。

### budgetter-front

- Nuxt.jsを使ったフロントエンド。
- ビルド時に`NUXT_PUBLIC_API_BASE_URL`を引数として受け取る。
- ビルド成果物を`budgetter_nuxt_dist`ボリュームに保存。

### budgetter-nginx

- Nginx 1.27.5を使用。
- ポート8082でホストに公開。
- 静的ファイルやNuxtのビルド成果物を配信。

---

## 4. 停止・再起動

```bash
docker compose stop
docker compose start
docker compose restart
```

---

## 5. ログ確認

```bash
docker compose logs -f [サービス名]
```

例:

```bash
docker compose logs -f budgetter-api
```

---

## 6. 注意事項

- `.env`および`.env.budgetter-api`は`setup.sh`で生成されます。
- MySQLの初期パスワードやAPIの設定は`.env`で管理。
- Dockerボリュームは必要に応じてバックアップしてください。

---

以上、家計簿アプリBudgetterのDocker環境セットアップ手順です。
