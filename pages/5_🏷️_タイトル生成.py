"""タイトル・見出し生成ツール。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="タイトル生成", page_icon="🏷️", layout="wide")
setup_sidebar()

st.title("🏷️ タイトル・見出し生成")
st.caption("記事の概要や本文から、複数のタイトル案を生成します。")

with st.form("title_form"):
    content = st.text_area(
        "記事の概要 or 本文",
        height=200,
        placeholder="タイトルを付けたい記事の概要、もしくは本文をそのまま貼り付けてください。",
    )

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "スタイル",
            ["SEOを意識した検索されやすいタイトル", "クリックしたくなるキャッチーなタイトル", "シンプルで分かりやすいタイトル", "数字を使ったリスト形式タイトル"],
        )
    with col2:
        count = st.slider("生成数", min_value=3, max_value=10, value=5)

    submitted = st.form_submit_button("タイトルを生成", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not content.strip():
        st.error("記事の概要または本文を入力してください。")
        st.stop()

    prompt = f"""以下の記事内容に対して、「{style}」の方向性でタイトル案を{count}個生成してください。

# 記事内容
{content}

出力は番号付きの箇条書きのみとし、各タイトルの前後に説明文は付けないでください。
"""

    with st.spinner("タイトルを生成しています..."):
        try:
            result = generate(prompt, temperature=0.9)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="titles.txt")
