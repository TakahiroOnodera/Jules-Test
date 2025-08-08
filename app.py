from flask import Flask, render_template, jsonify
import logging

app = Flask(__name__)

# 詳細なログ設定
# コンソールにログを出力するハンドラを設定
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s : %(message)s',
                    handlers=[logging.StreamHandler()])

# サンプルのニュースデータ
# 本来はデータベースや外部APIから取得する
DUMMY_NEWS_DATA = [
    {
        "id": 1,
        "title": "次世代AI、人間レベルの推論能力を達成か",
        "url": "https://example.com/news1"
    },
    {
        "id": 2,
        "title": "新しい量子コンピュータが計算速度の記録を更新",
        "url": "https://example.com/news2"
    },
    {
        "id": 3,
        "title": "スタートアップ企業、画期的なバッテリー技術を発表",
        "url": "https://example.com/news3"
    },
    {
        "id": 4,
        "title": "サイバーセキュリティの新たな脅威：AIによるフィッシング攻撃",
        "url": "https://example.com/news4"
    },
    {
        "id": 5,
        "title": "火星探査ミッション、重要な地質学的発見を報告",
        "url": "https://example.com/news5"
    }
]

@app.route('/')
def index():
    """
    フロントエンドのメインページをレンダリングする。
    """
    app.logger.info("トップページへのアクセスがありました。index.htmlを返します。")
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    """
    ニュース記事のリストをJSON形式で返すAPIエンドポイント。
    """
    app.logger.info(f"/api/news へのリクエストがありました。{len(DUMMY_NEWS_DATA)}件のニュースデータを返します。")
    try:
        return jsonify(DUMMY_NEWS_DATA)
    except Exception as e:
        app.logger.error(f"ニュースデータのJSON変換中にエラーが発生しました: {e}", exc_info=True)
        return jsonify({"error": "サーバー内部でエラーが発生しました。"}), 500

if __name__ == '__main__':
    # debug=True は開発時には便利ですが、本番環境ではFalseにすべきです。
    app.run(host='0.0.0.0', port=5000, debug=True)
