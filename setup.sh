#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

copy_if_not_exists() {
  local src="$1"
  local dst="$2"
  if [ -e "$dst" ]; then
    echo "⚠️ $dst は既に存在するためスキップしました"
  else
    cp "$src" "$dst"
    echo "✅ $src → $dst"
  fi
}

copy_if_not_exists "$SCRIPT_DIR/docker/.env.example" "$SCRIPT_DIR/.env"
copy_if_not_exists "$SCRIPT_DIR/docker/budgetter-api/.env.example" "$SCRIPT_DIR/.env.budgetter-api"
