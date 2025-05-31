FROM ubuntu:24.04

# 必要パッケージをインストール
RUN apt-get update && apt-get install -y \
    python3.12 python3.12-venv python3.12-dev \
    libapache2-mod-wsgi-py3 apache2 mariadb-client\
    build-essential curl git vim tzdata\
    pkg-config default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app/budgetter-api

# アプリコードをコピー
COPY ./budgetter-api .

# venv 作成とパッケージインストール
RUN python3.12 -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# Apache mod_wsgi 設定
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Entrypoint スクリプトをコピー
COPY docker/budgetter-api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 環境変数で PATH に venv を追加（任意）
ENV PATH="/app/budgetter-api/.venv/bin:$PATH"

ENV TZ=Asia/Tokyo

# 起動
ENTRYPOINT ["/entrypoint.sh"]
