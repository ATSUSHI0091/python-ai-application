"""文章要約ツール。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
setup_sidebar()

st.title("📄 文章要約")
st.caption("長い文章を、指定した長さ・形式で要約します。")

with st.form("summary_form"):
    source_text = st.text_area(
        "要約したい文章",
        height=300,
        placeholder="記事、議事録、論文など、要約したいテキストを貼り付けてください。",
    )

    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox(
            "要約の長さ",
            ["一言（1文）", "短め（3行程度）", "標準（5〜7行）", "詳細（元の30%程度）"],
            index=2,
        )
    with col2:
        style = st.selectbox("形式", ["箇条書き", "文章（段落形式）"])

    focus = st.text_input("特に重視したい観点（任意）", placeholder="例: 結論と数値データを中心に")

    submitted = st.form_submit_button("要約する", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not source_text.strip():
        st.error("要約したい文章を入力してください。")
        st.stop()

    prompt = f"""以下の文章を要約してください。

# 要約の長さ
{length}

# 形式
{style}

# 重視したい観点
{focus or "特になし（全体をバランスよく）"}

# 要約対象の文章
{source_text}

余計な前置き（「以下が要約です」等）は不要です。要約結果のみを出力してください。
"""

    with st.spinner("要約しています..."):
        try:
            result = generate(prompt, temperature=0.3)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="summary.txt")
