"""キーワード抽出ツール。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="キーワード抽出", page_icon="🔑", layout="wide")
setup_sidebar()

st.title("🔑 キーワード抽出")
st.caption("文章からSEOやタグ付けに使えるキーワードを抽出します。")

PURPOSE_INSTRUCTIONS = {
    "SEOキーワード（検索されやすい語句）": "検索エンジンで上位表示を狙う際に有効な、検索需要がありそうなキーワードを優先してください。",
    "ブログ・SNSのタグ付け": "記事のタグやハッシュタグとしてそのまま使える、短く簡潔な語句を優先してください。",
    "文章内の重要語（要点把握用）": "文章の主旨を理解する上で重要な固有名詞・専門用語・キーフレーズを優先してください。",
}

with st.form("keyword_form"):
    source_text = st.text_area(
        "対象の文章",
        height=250,
        placeholder="キーワードを抽出したい文章（記事本文、企画メモなど）を貼り付けてください。",
    )

    col1, col2 = st.columns(2)
    with col1:
        purpose = st.selectbox("抽出の目的", list(PURPOSE_INSTRUCTIONS.keys()))
    with col2:
        count = st.slider("抽出数の目安", min_value=5, max_value=20, value=10)

    submitted = st.form_submit_button("キーワードを抽出", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not source_text.strip():
        st.error("対象の文章を入力してください。")
        st.stop()

    prompt = f"""以下の文章から、キーワードを{count}個程度抽出してください。

# 抽出の目的
{purpose}
{PURPOSE_INSTRUCTIONS[purpose]}

# 対象の文章
{source_text}

出力は「キーワード（重要度順の箇条書き）」のみとし、各項目に一言で簡単な補足（なぜ重要か）を添えてください。
前置きの説明文は不要です。
"""

    with st.spinner("キーワードを抽出しています..."):
        try:
            result = generate(prompt, temperature=0.3)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="keywords.txt")
