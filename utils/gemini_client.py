"""Gemini API とのやり取りをまとめたヘルパーモジュール。"""
from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

AVAILABLE_MODELS = {
    "Gemini 3.6 Flash（高速・低コスト）": "models/gemini-3.6-flash",
    "Gemini 2.5 Pro（高品質）": "gemini-2.5-pro",
}
DEFAULT_MODEL_LABEL = "Gemini 3.6 Flash（高速・低コスト）"


def get_api_key() -> str | None:
    """セッション状態 → 環境変数 の順で API キーを探す。"""
    return st.session_state.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")


def has_api_key() -> bool:
    return bool(get_api_key())


@st.cache_resource(show_spinner=False)
def _get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def generate(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.7,
    model_name: str | None = None,
) -> str:
    """プロンプトを Gemini に投げてテキストを返す。

    APIキー未設定やAPIエラー時は RuntimeError を送出する。
    """
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "Gemini APIキーが設定されていません。サイドバーから入力するか、"
            "環境変数 GEMINI_API_KEY を設定してください。"
        )

    model_name = model_name or st.session_state.get(
        "gemini_model", AVAILABLE_MODELS[DEFAULT_MODEL_LABEL]
    )

    try:
        client = _get_client(api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_instruction,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - APIエラーをそのまま画面に出すため
        raise RuntimeError(f"Gemini APIの呼び出しに失敗しました: {exc}") from exc

    if not response.text:
        raise RuntimeError("Gemini APIから空の応答が返されました。")

    return response.text
