"""文章校正・リライトツール。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="文章校正・リライト", page_icon="🩹", layout="wide")
setup_sidebar()

st.title("🩹 文章校正・リライト")
st.caption("誤字脱字のチェックや、目的に合わせた文章のリライトを行います。")

MODE_PROMPTS = {
    "誤字脱字・文法チェック": (
        "誤字脱字、文法の誤り、不自然な表現のみを修正してください。文体や内容は変えないでください。"
        "修正した文章に加えて、どこをどう直したか簡単な説明も付けてください。"
    ),
    "自然な文章に整える": "意味を変えずに、より自然で読みやすい日本語に整えてください。",
    "丁寧な表現にする": "内容は変えずに、丁寧でフォーマルな表現にリライトしてください。",
    "カジュアルにする": "内容は変えずに、親しみやすくカジュアルな表現にリライトしてください。",
    "簡潔にする": "内容の要点は保ったまま、できるだけ簡潔に短くリライトしてください。",
    "詳しく肉付けする": "内容の骨子は保ったまま、説明や具体例を加えて詳しく肉付けしてください。",
}

with st.form("rewrite_form"):
    source_text = st.text_area("元の文章", height=250, placeholder="校正・リライトしたい文章を貼り付けてください。")
    mode = st.selectbox("モード", list(MODE_PROMPTS.keys()))
    submitted = st.form_submit_button("実行", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not source_text.strip():
        st.error("元の文章を入力してください。")
        st.stop()

    instruction = MODE_PROMPTS[mode]
    show_diff = mode == "誤字脱字・文法チェック"

    prompt = f"""あなたは日本語のプロの校正者・編集者です。以下の文章に対して次の指示を実行してください。

# 指示
{instruction}

# 元の文章
{source_text}

{"出力形式は「## 修正後の文章」の見出しの後に修正した文章、続けて「## 修正箇所の説明」の見出しの後に変更点の説明を箇条書きで記載してください。" if show_diff else "修正・リライトした文章のみを出力してください。前置きは不要です。"}
"""

    with st.spinner("処理しています..."):
        try:
            result = generate(prompt, temperature=0.4)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="rewritten.txt")
