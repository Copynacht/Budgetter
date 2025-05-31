#!/bin/bash

# スクリプトが存在するディレクトリを基準に動作
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# ファイルコピー処理
cp "$SCRIPT_DIR/docker/.env.example" "$SCRIPT_DIR/.env"
echo "✅ docker/.env.example → .env"

cp "$SCRIPT_DIR/docker/budgetter-api/.env.example" "$SCRIPT_DIR/docker/.env.budgetter-api"
echo "✅ docker/budgetter-api/.env.example → .env.budgetter-api"
