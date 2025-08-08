document.addEventListener('DOMContentLoaded', function() {
    const newsList = document.getElementById('news-list');

    // バックエンドAPIからニュースデータを非同期で取得する
    fetch('/api/news')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(newsData => {
            // ニュースデータが空の場合のメッセージ
            if (!newsData || newsData.length === 0) {
                newsList.innerHTML = '<li>ニュース記事が見つかりませんでした。</li>';
                return;
            }

            // 取得したデータでリストを生成
            newsData.forEach(article => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = article.url;
                link.textContent = article.title;
                link.target = '_blank'; // 新しいタブで開く

                listItem.appendChild(link);
                newsList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('ニュースの取得に失敗しました:', error);
            newsList.innerHTML = '<li>ニュースの読み込み中にエラーが発生しました。</li>';
        });
});
