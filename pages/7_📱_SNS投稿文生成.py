"""SNS投稿文生成ツール。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="SNS投稿文生成", page_icon="📱", layout="wide")
setup_sidebar()

st.title("📱 SNS投稿文生成")
st.caption("トピックや記事の内容から、SNSプラットフォームに合わせた投稿文を生成します。")

PLATFORM_RULES = {
    "X（Twitter）": "全角換算で140字程度に収まる、テンポの良い文章にする。",
    "Instagram": "冒頭で惹きつけ、改行を効果的に使った読みやすいキャプションにする（300〜500字程度）。",
    "LinkedIn": "ビジネス・専門性を意識した、やや長めで説得力のある文章にする（300〜600字程度）。",
    "Facebook": "親しみやすく、共感を呼ぶ文章にする（200〜400字程度）。",
}

with st.form("sns_form"):
    content = st.text_area(
        "投稿のもとになる内容",
        height=200,
        placeholder="伝えたいトピック、告知内容、記事の要約などを入力してください。",
    )

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("プラットフォーム", list(PLATFORM_RULES.keys()))
    with col2:
        count = st.slider("生成する投稿案の数", min_value=1, max_value=5, value=3)

    col3, col4 = st.columns(2)
    with col3:
        tone = st.selectbox("トーン", ["親しみやすい", "熱意が伝わる", "フォーマル", "ユーモアを交える"])
    with col4:
        use_hashtags = st.checkbox("ハッシュタグを含める", value=True)

    submitted = st.form_submit_button("投稿文を生成", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not content.strip():
        st.error("投稿のもとになる内容を入力してください。")
        st.stop()

    hashtag_instruction = (
        "各案の最後に関連性の高いハッシュタグを3〜5個付けてください。"
        if use_hashtags
        else "ハッシュタグは付けないでください。"
    )

    prompt = f"""あなたはSNS運用のプロです。以下の内容をもとに、{platform}向けの投稿文を{count}パターン作成してください。

# 投稿のもとになる内容
{content}

# プラットフォームのルール
{PLATFORM_RULES[platform]}

# トーン
{tone}

# ハッシュタグ
{hashtag_instruction}

各案は「案1」「案2」のように見出しを付けて区切ってください。前置きの説明は不要です。
"""

    with st.spinner("投稿文を生成しています..."):
        try:
            result = generate(prompt, temperature=0.9)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="sns_posts.txt")
