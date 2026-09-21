# AIライティングツール

Gemini APIを使った個人用のAIライティング支援ツールです。データベースや認証機能は持たず、
ローカル（またはローカル同等のセッション）でそのまま使うことを想定しています。

## 搭載機能

- 📝 ブログ記事作成
- 📧 メール返信作成
- 📄 文章要約
- 🩹 文章校正・リライト
- 🏷️ タイトル・見出し生成
- 🌐 翻訳
- 📱 SNS投稿文生成
- 🔑 キーワード抽出

## セットアップ

1. 依存パッケージをインストール

   ```bash
   pip install -r requirements.txt
   ```

2. Gemini APIキーを設定（どちらか一方でOK）

   - `.env.example` を `.env` にコピーして `GEMINI_API_KEY` を設定する
   - もしくは、アプリ起動後にサイドバーから直接APIキーを入力する（保存はされず、セッション中のみ有効）

3. アプリを起動

   ```bash
   streamlit run app.py
   ```

## 動作確認

依存パッケージのインポート、全ファイルの構文、APIキーの設定、Gemini APIへの疎通を
まとめてチェックできる。

```bash
python check_setup.py
```

## 技術スタック

- Python
- Streamlit（マルチページアプリ）
- Gemini API（`google-genai` SDK）
