"""メール返信作成ツール。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="メール返信作成", page_icon="📧", layout="wide")
setup_sidebar()

st.title("📧 メール返信作成")
st.caption("受信したメールと返信の要点を入力すると、返信文の下書きを作成します。")

with st.form("email_form"):
    original_email = st.text_area(
        "受信したメール本文",
        height=200,
        placeholder="返信元のメール本文を貼り付けてください（任意：新規メールの場合は空欄でもOK）",
    )
    reply_points = st.text_area(
        "返信で伝えたい内容・要点",
        height=120,
        placeholder="例: 会議の日程は来週火曜14時でお願いしたい。資料は今週中に送ります。",
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "トーン",
            ["丁寧・フォーマル（社外向け）", "丁寧・親しみやすい（社内向け）", "簡潔・ビジネスライク", "カジュアル"],
        )
    with col2:
        language = st.selectbox("言語", ["日本語", "英語"])

    sender_name = st.text_input("差出人名（署名に使用、任意）", placeholder="例: 大畑")

    submitted = st.form_submit_button("返信文を生成", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not reply_points.strip():
        st.error("返信で伝えたい内容・要点を入力してください。")
        st.stop()

    prompt = f"""あなたは優秀なビジネスパーソンの秘書です。以下の情報をもとにメールの返信文を作成してください。

# 受信したメール本文（参考）
{original_email or "（新規メール、または受信メールなし）"}

# 返信で伝えたい内容・要点
{reply_points}

# トーン
{tone}

# 言語
{language}

# 署名
{sender_name or "（署名なし、または「よろしくお願いいたします」のみで締める）"}

件名は付けず、本文のみを出力してください。宛名（〇〇様）から始め、要点を過不足なく盛り込み、
読み手に失礼のない自然な文章にしてください。
"""

    with st.spinner("返信文を生成しています..."):
        try:
            result = generate(prompt, temperature=0.6)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="email_reply.txt")
