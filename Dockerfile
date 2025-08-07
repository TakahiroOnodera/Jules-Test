# Pythonの公式イメージをベースとして使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Flaskアプリケーションが使用するポートを公開
EXPOSE 5000

# アプリケーションを実行するコマンド
CMD ["python", "app.py"]
