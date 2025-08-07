from flask import Flask, render_template, request, jsonify
import logging
import random
import string

app = Flask(__name__)

# 詳細なログ設定
# ファイルに出力する場合は、FileHandlerを追加します。
# logging.basicConfig(filename='app.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])


# --- パスワード生成ロジック ---

# 文字変換のルール
TRANSFORMATION_MAP = {
    'l': '1', 'o': '0', 's': '5', 'q': '9', 'b': '8',
    'L': '1', 'O': '0', 'S': '5', 'Q': '9', 'B': '8'
}

# 文字セットの定義
CHAR_SETS = {
    'upper': string.ascii_uppercase,
    'lower': string.ascii_lowercase,
    'numbers': string.digits,
    'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?'
}

def generate_password(char_types, length, base_word):
    """パスワードを生成するメイン関数"""
    app.logger.info(f"パスワード生成開始: length={length}, char_types={char_types}, base_word='{base_word}'")

    # 1. ベースとなる文字リストを作成
    password_chars = []
    if base_word:
        # 指定単語の文字を変換
        for char in base_word:
            password_chars.append(TRANSFORMATION_MAP.get(char, char))
        app.logger.debug(f"指定単語を変換後: {''.join(password_chars)}")

    # 2. 使用する文字のプールを作成
    char_pool = ''
    if not char_types: # もし文字種が選択されなかった場合のフォールバック
        app.logger.warning("文字種が選択されていません。デフォルトの文字種（小文字）を使用します。")
        char_pool += CHAR_SETS['lower']
    else:
        for char_type in char_types:
            char_pool += CHAR_SETS.get(char_type, '')

    if not char_pool:
        raise ValueError("有効な文字種が選択されていません。")

    # 3. 最低でも各文字種が1つは含まれるようにする (もし選択されていれば)
    guaranteed_chars = []
    if len(password_chars) < length:
        for char_type in char_types:
            if char_type in CHAR_SETS:
                guaranteed_chars.append(random.choice(CHAR_SETS[char_type]))

    password_chars.extend(guaranteed_chars)
    app.logger.debug(f"必須文字を追加後: {''.join(password_chars)}")


    # 4. 残りの文字をランダムに追加
    remaining_length = length - len(password_chars)
    if remaining_length > 0:
        for _ in range(remaining_length):
            password_chars.append(random.choice(char_pool))
    app.logger.debug(f"ランダム文字を追加後: {''.join(password_chars)}")

    # 5. 文字数が指定より多い場合は切り詰める
    if len(password_chars) > length:
        password_chars = password_chars[:length]
        app.logger.debug(f"長さを{length}に調整後: {''.join(password_chars)}")

    # 6. 大文字・小文字をランダムに変換 (50%の確率)
    for i, char in enumerate(password_chars):
        if char.isalpha() and random.random() < 0.5:
            password_chars[i] = char.swapcase()
    app.logger.debug(f"大文字小文字変換後: {''.join(password_chars)}")

    # 7. パスワードをシャッフル
    random.shuffle(password_chars)
    final_password = "".join(password_chars)

    app.logger.info(f"生成されたパスワード: {final_password}")
    return final_password


# --- Flaskルート ---

@app.route('/')
def index():
    app.logger.info("トップページへのアクセスがありました。")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def handle_generate():
    """フロントエンドからのリクエストを処理し、パスワードを生成して返す"""
    try:
        data = request.get_json()
        app.logger.debug(f"受信したリクエストデータ: {data}")

        char_types = data.get('char_types', [])
        length = data.get('length', 12)
        base_word = data.get('base_word', '')

        # バリデーション
        if not isinstance(length, int) or not (4 <= length <= 100):
            raise ValueError("文字数は4から100の間で指定してください。")
        if not isinstance(char_types, list):
            raise ValueError("文字種はリスト形式で指定してください。")

        password = generate_password(char_types, length, base_word)
        return jsonify({'password': password})

    except ValueError as e:
        app.logger.error(f"入力値エラー: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"予期せぬエラーが発生しました: {e}", exc_info=True)
        return jsonify({'error': 'サーバー内部でエラーが発生しました。'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
