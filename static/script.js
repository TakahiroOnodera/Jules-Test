document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('password-form');
    const resultContainer = document.getElementById('result-container');
    const passwordOutput = document.getElementById('password-output');
    const customLengthInput = document.getElementById('custom_length');
    const otherLengthRadio = document.getElementById('len_other');

    // 「その他」の文字数入力が変更されたら、対応するラジオボタンを選択状態にする
    customLengthInput.addEventListener('input', () => {
        otherLengthRadio.checked = true;
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // デフォルトのフォーム送信をキャンセル

        // 1. フォームからデータを収集
        const charTypes = Array.from(document.querySelectorAll('input[name="char_types"]:checked'))
                               .map(cb => cb.value);

        let length;
        const lengthOption = document.querySelector('input[name="length_option"]:checked').value;
        if (lengthOption === 'other') {
            length = parseInt(customLengthInput.value, 10);
        } else {
            length = parseInt(lengthOption, 10);
        }

        const baseWord = document.getElementById('base_word').value;

        // 2. バックエンドにデータを送信
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    char_types: charTypes,
                    length: length,
                    base_word: baseWord
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'パスワードの生成に失敗しました。');
            }

            const data = await response.json();

            // 3. 結果を表示
            if (data.password) {
                passwordOutput.textContent = data.password;
                resultContainer.style.display = 'block';
            } else if (data.error) {
                 throw new Error(data.error);
            }

        } catch (error) {
            passwordOutput.textContent = `エラー: ${error.message}`;
            resultContainer.style.display = 'block';
        }
    });
});
