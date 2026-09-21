"""セットアップの動作確認用スクリプト。

使い方:
    python check_setup.py

依存パッケージのインポート、全ファイルの構文チェック、APIキーの有無、
（キーが設定されていれば）Gemini APIへの疎通確認をまとめて行う。
"""
from __future__ import annotations

import glob
import os
import py_compile
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Windows環境（cp932など）でも絵文字混じりの出力が文字化けしないようにする。
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")


def check_imports() -> bool:
    try:
        import streamlit  # noqa: F401
        from google import genai  # noqa: F401
        import dotenv  # noqa: F401
    except ImportError as e:
        print(f"❌ 依存パッケージ: インポートに失敗しました ({e})")
        print("   → `pip install -r requirements.txt` を実行してください。")
        return False
    print("✅ 依存パッケージ: streamlit / google-genai / python-dotenv のインポートに成功")
    return True


def check_syntax() -> bool:
    py_files = (
        [os.path.join(BASE_DIR, "app.py"), os.path.join(BASE_DIR, "check_setup.py")]
        + glob.glob(os.path.join(BASE_DIR, "pages", "*.py"))
        + glob.glob(os.path.join(BASE_DIR, "utils", "*.py"))
    )

    all_ok = True
    for f in py_files:
        try:
            py_compile.compile(f, doraise=True)
        except py_compile.PyCompileError as e:
            print(f"❌ 構文チェック: {os.path.relpath(f, BASE_DIR)} でエラー\n{e}")
            all_ok = False

    if all_ok:
        print(f"✅ 構文チェック: {len(py_files)}個のファイルすべてOK")
    return all_ok


def check_api_key() -> str | None:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(BASE_DIR, ".env"))
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key:
        print("✅ APIキー: 環境変数 GEMINI_API_KEY が設定されています")
    else:
        print(
            "⚠️  APIキー: 環境変数 GEMINI_API_KEY が未設定です"
            "（.envファイルを作成するか、アプリ起動後にサイドバーから入力してください）"
        )
    return api_key


def check_gemini_connection(api_key: str | None) -> bool:
    if not api_key:
        print("⏭  Gemini API疎通確認: APIキー未設定のためスキップ")
        return True

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="models/gemini-3.6-flash",
            contents="動作確認です。「OK」とだけ返してください。",
        )
        if not response.text:
            print("❌ Gemini API疎通確認: 応答が空でした")
            return False
        print(f"✅ Gemini API疎通確認: 成功（応答: {response.text.strip()[:30]}）")
        return True
    except Exception as e:  # noqa: BLE001
        print(f"❌ Gemini API疎通確認: 失敗しました ({e})")
        return False


def main() -> int:
    print("=== AIライティングツール 動作確認 ===\n")

    results = [
        check_imports(),
        check_syntax(),
    ]
    api_key = check_api_key()
    results.append(check_gemini_connection(api_key))

    print()
    if all(results):
        print("すべてのチェックに合格しました。`streamlit run app.py` で起動できます。")
        return 0

    print("いくつかの項目に問題があります。上記のメッセージを確認してください。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
