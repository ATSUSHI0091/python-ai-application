"""ページ共通のUI部品。"""
from __future__ import annotations

import streamlit as st

from utils.gemini_client import AVAILABLE_MODELS, DEFAULT_MODEL_LABEL, has_api_key


def setup_sidebar() -> None:
    """APIキー入力とモデル選択をサイドバーに表示する。全ページ共通。"""
    with st.sidebar:
        st.subheader("⚙️ Gemini API 設定")

        current_key = st.session_state.get("gemini_api_key", "")
        api_key_input = st.text_input(
            "APIキー",
            value=current_key,
            type="password",
            help="環境変数 GEMINI_API_KEY を設定済みの場合は空欄のままでOKです。",
            placeholder="環境変数を使う場合は空欄でOK",
        )
        if api_key_input:
            st.session_state["gemini_api_key"] = api_key_input

        model_label = st.selectbox(
            "使用モデル",
            options=list(AVAILABLE_MODELS.keys()),
            index=list(AVAILABLE_MODELS.keys()).index(DEFAULT_MODEL_LABEL),
        )
        st.session_state["gemini_model"] = AVAILABLE_MODELS[model_label]

        if has_api_key():
            st.success("APIキー設定済み", icon="✅")
        else:
            st.warning("APIキー未設定", icon="⚠️")

        st.divider()
        st.caption(
            "個人利用向けのAIライティングツールです。\n"
            "入力内容やAPIキーは外部に保存されず、このセッション内のみで利用されます。"
        )


def show_result(text: str, *, filename: str = "result.txt") -> None:
    """生成結果を表示し、コピー用テキストエリアとダウンロードボタンを付ける。"""
    st.markdown("### 生成結果")
    st.markdown(text)
    with st.expander("コピー用テキスト / ダウンロード"):
        st.text_area("プレーンテキスト", value=text, height=200)
        st.download_button(
            "テキストファイルとしてダウンロード",
            data=text,
            file_name=filename,
            mime="text/plain",
        )


def require_api_key_notice() -> bool:
    """APIキーが無ければ警告を表示してTrueを返す(呼び出し側でreturnする)。"""
    if not has_api_key():
        st.info("👈 サイドバーからGemini APIキーを入力してください。")
        return True
    return False
