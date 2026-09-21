# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## これは何か

Streamlit と Gemini API で作った個人用のAIライティング支援アプリ。データベースも認証もない、
1ユーザー・ローカル前提のアプリ。APIキーは `.env`(`GEMINI_API_KEY`)経由、またはサイドバーから
実行時に入力する(`st.session_state` に保持されるだけで、どこにも永続化されない)。

## コマンド

```bash
pip install -r requirements.txt
streamlit run app.py            # デフォルトで localhost:8501 で起動
```

テストスイート・リンター・ビルド手順は用意されていない。代わりに `check_setup.py` という
簡易チェックスクリプトがある(依存パッケージのimport確認、`pages/` と `utils/` 配下の全ファイルの
構文チェック、`GEMINI_API_KEY` の設定確認、キーがあれば実際にGemini APIへ1回だけ疎通確認の
リクエストを送る)。変更を加えたときは、これを実行してから実際にアプリを起動し該当ページを
ブラウザで動かして確認する。

```bash
python check_setup.py
```

## アーキテクチャ

**Streamlitのマルチページアプリ。** `app.py` がホーム画面で、各ツールは `pages/` 配下にあり、
Streamlitがファイル名から自動的にページとして認識する。ファイル名の先頭の数字がサイドバー内の
表示順を決め、ファイル名中の絵文字がサイドバーのアイコンになる。ページを追加する際は両方とも
このルールに合わせること。

```
pages/N_<絵文字>_<名前>.py
```

**共通ロジックはページ側ではなく `utils/` に置く:**
- `utils/gemini_client.py` — Geminiと通信する唯一の窓口(`google-genai` SDK の
  `google.genai.Client` を使用)。`generate(prompt, system_instruction=None, temperature=0.7,
  model_name=None)` を公開している。APIキーは `get_api_key()` で取得し(まず session state、
  次に環境変数 `GEMINI_API_KEY` の順)、キー未設定やAPI呼び出し失敗時は `RuntimeError` を送出する
  — 各ページ側でこれを catch して `st.error()` で表示する設計で、ページをクラッシュさせない。
  `genai.Client` のインスタンスは APIキーごとに `st.cache_resource` でキャッシュされる。
- `utils/ui.py` — `setup_sidebar()`(APIキー入力欄とモデル選択、各ページの冒頭で必ず呼ぶ)、
  `show_result()`(生成結果の表示＋コピー用テキストエリア/ダウンロードのexpanderを表示)、
  `require_api_key_notice()`(各ページは `setup_sidebar()` の直後にこれを呼び、`True` が返って
  きたら `st.stop()` する)。

**ページの共通パターン。** `pages/` 配下の各ページは全て同じ構成に従う: `st.set_page_config()`
→ `setup_sidebar()` → `st.form(...)` の中に入力項目を並べる → 送信時に
`require_api_key_notice()` をチェック → 必須項目のバリデーション → 日本語のプロンプト文字列を
組み立てる → `try/except RuntimeError` で `generate(...)` を呼ぶ → `show_result(...)`。
新しいライティングツールを追加する際は、新しい構成を考えるのではなくこのパターンを踏襲すること。

**モデル。** 利用可能なGeminiモデルは `gemini_client.py` 内の `AVAILABLE_MODELS` で定義されて
おり(現在は Flash/Pro 2.5)、サイドバーのセレクトボックスにそのラベルが表示される。選択された
モデル名は `st.session_state["gemini_model"]` に格納され `generate()` が参照する。モデルを
追加する場合はページ側に直接書かず、ここに追加すること。

ユーザー向けの文字列(ラベル、Geminiに送るプロンプト、エラーメッセージ)は全て日本語。新しい
ページを追加する際もこれに合わせる。
