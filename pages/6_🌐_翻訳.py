"""翻訳ツール。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="wide")
setup_sidebar()

st.title("🌐 翻訳")
st.caption("文章を、トーンを保ちながら指定した言語に翻訳します。")

LANGUAGES = ["英語", "日本語", "中国語（簡体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語"]

with st.form("translate_form"):
    source_text = st.text_area("翻訳したい文章", height=250, placeholder="翻訳したい文章を貼り付けてください。")

    col1, col2 = st.columns(2)
    with col1:
        target_language = st.selectbox("翻訳先の言語", LANGUAGES)
    with col2:
        tone = st.selectbox("トーン", ["自然な標準的表現", "ビジネス・フォーマル", "カジュアル・親しみやすい"])

    submitted = st.form_submit_button("翻訳する", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not source_text.strip():
        st.error("翻訳したい文章を入力してください。")
        st.stop()

    prompt = f"""以下の文章を{target_language}に翻訳してください。

# トーン
{tone}

# 元の文章
{source_text}

直訳ではなく、自然で意味の通じる翻訳にしてください。翻訳結果のみを出力し、前置きや解説は不要です。
"""

    with st.spinner("翻訳しています..."):
        try:
            result = generate(prompt, temperature=0.3)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="translation.txt")
