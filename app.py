"""AIライティングツール - ホーム画面。"""
import streamlit as st

from utils.ui import setup_sidebar

st.set_page_config(
    page_title="AIライティングツール",
    page_icon="✍️",
    layout="wide",
)

setup_sidebar()

st.title("✍️ AIライティングツール")
st.caption("Gemini APIを活用した個人用ライティング支援ツール集")

st.markdown(
    """
左のサイドバーからツールを選んでください。初回利用時は、サイドバー上部で
**Gemini APIキー** を入力するか、環境変数 `GEMINI_API_KEY` を設定してください。
"""
)

st.divider()

tools = [
    ("📝", "ブログ記事作成", "テーマとキーワードから見出し付きのブログ記事を自動生成します。"),
    ("📧", "メール返信作成", "受信メールと返信の要点を入力するだけで、丁寧な返信文を作成します。"),
    ("📄", "文章要約", "長い文章を指定した長さ・形式で要約します。"),
    ("🩹", "文章校正・リライト", "誤字脱字のチェックや、トーンを変えたリライトを行います。"),
    ("🏷️", "タイトル生成", "記事の概要から複数のタイトル・見出し案を生成します。"),
    ("🌐", "翻訳", "文章を指定した言語に、トーンを保ちながら翻訳します。"),
    ("📱", "SNS投稿文生成", "トピックや記事の内容から、プラットフォームに合わせたSNS投稿文を作成します。"),
    ("🔑", "キーワード抽出", "文章からSEOやタグ付けに使えるキーワードを抽出します。"),
]

cols = st.columns(3)
for i, (icon, name, desc) in enumerate(tools):
    with cols[i % 3]:
        st.markdown(f"#### {icon} {name}")
        st.write(desc)
        st.markdown("")

st.divider()
st.caption(
    "このアプリはデータベースや認証機能を持たない個人用ツールです。"
    "入力データやAPIキーはブラウザのセッション内でのみ保持され、サーバー側には保存されません。"
)
