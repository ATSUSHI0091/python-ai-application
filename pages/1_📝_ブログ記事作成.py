"""ブログ記事作成ツール（SEO対応）。"""
import streamlit as st

from utils.gemini_client import generate
from utils.ui import require_api_key_notice, setup_sidebar, show_result

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")
setup_sidebar()

st.title("📝 ブログ記事作成")
st.caption("SEOを意識した、見出し付きのブログ記事を作成します。")

with st.form("blog_form"):
    topic = st.text_input("テーマ・タイトル案", placeholder="例: 在宅ワークの生産性を上げる方法")
    main_keyword = st.text_input(
        "メインキーワード（SEOで上位表示を狙う語句）",
        placeholder="例: 在宅ワーク 生産性",
        help="検索されたい語句を1つ指定してください。タイトル・導入文・見出しに自然に含めます。",
    )
    sub_keywords = st.text_input(
        "関連・サブキーワード（カンマ区切り、任意）",
        placeholder="例: タイムマネジメント, 集中力, ツール",
    )
    audience = st.text_input("想定読者（任意）", placeholder="例: リモートワーク初心者の会社員")

    col1, col2 = st.columns(2)
    with col1:
        search_intent = st.selectbox(
            "検索意図（読者が何を求めて検索しているか）",
            [
                "知りたい・調べたい（情報収集）",
                "比較・検討したい（複数の選択肢を比べたい）",
                "やり方・使い方を知りたい（ハウツー）",
                "購入・申込を検討している",
            ],
        )
    with col2:
        tone = st.selectbox(
            "文体・トーン",
            ["丁寧・解説調", "カジュアル・親しみやすい", "専門的・データ重視", "エッセイ調"],
        )

    length = st.selectbox(
        "文章量の目安",
        ["短め（600〜800字）", "標準（1200〜1500字）", "長め（2000字以上）"],
        index=1,
    )

    col3, col4 = st.columns(2)
    with col3:
        include_title_suggestions = st.checkbox("SEOタイトル案も生成する（複数案）", value=True)
    with col4:
        include_meta_description = st.checkbox("メタディスクリプションも生成する", value=True)

    include_structure = st.checkbox("見出し（H2/H3）構成にする", value=True, help="SEO上は基本的にON推奨です。")
    extra_notes = st.text_area("その他の要望（任意）", placeholder="例: 具体例を3つ入れてほしい")

    submitted = st.form_submit_button("記事を生成", type="primary")

if require_api_key_notice():
    st.stop()

if submitted:
    if not topic.strip():
        st.error("テーマ・タイトル案を入力してください。")
        st.stop()
    if not main_keyword.strip():
        st.error("メインキーワードを入力してください。")
        st.stop()

    structure_instruction = (
        "Markdownの見出し（##, ###）を使って構成すること。各見出しにはメインキーワードや"
        "関連キーワードを不自然にならない範囲で盛り込むこと。"
        if include_structure
        else "見出しは使わず、自然な段落構成にすること。"
    )

    output_sections = []
    if include_title_suggestions:
        output_sections.append(
            "1. 「## SEOタイトル案」という見出しの下に、メインキーワードを含む32文字前後のタイトル案を3つ箇条書きで提示する。"
        )
    if include_meta_description:
        output_sections.append(
            "2. 「## メタディスクリプション」という見出しの下に、メインキーワードを含む120字前後の説明文を1つ提示する。"
        )
    output_sections.append(
        f"{len(output_sections) + 1}. 「## 本文」という見出しの下に、記事本文を執筆する。"
    )
    output_format_instruction = "\n".join(output_sections)

    prompt = f"""あなたはSEOに精通したプロのブログライター兼SEOライターです。
以下の条件でSEOを意識したブログ記事を執筆してください。

# テーマ
{topic}

# メインキーワード（最重要・検索上位を狙う語句）
{main_keyword}

# 関連・サブキーワード
{sub_keywords or "指定なし"}

# 検索意図
{search_intent}

# 想定読者
{audience or "指定なし"}

# 文体・トーン
{tone}

# 文章量の目安
{length}

# 構成
{structure_instruction}

# その他の要望
{extra_notes or "特になし"}

# SEO上の執筆ルール
- メインキーワードは、タイトル・導入文（リード文）・少なくとも1つの見出し・まとめの中に、
  不自然にならない範囲で自然に含めること（キーワードの詰め込みすぎは避ける）。
- 導入文（リード文）では、この記事を読むとどんな悩みが解決するか・何が分かるかを最初の2〜3文で
  明示し、読者の検索意図に早い段階で応えること。
- 見出し（H2/H3）は読者が知りたい疑問に沿って設計し、単なる装飾ではなく検索意図を反映した
  具体的な見出し文にすること。
- 抽象的な説明だけでなく、具体例・手順・数値などを交え、他の記事と差別化できる独自性のある
  内容にすること。
- 箇条書きや強調（太字）を適度に使い、スキャンして読める（流し読みしやすい）文章にすること。
- 記事の最後に、内容のまとめと読者の次の行動を促す一文（例: 今日から試してみましょう、等）を
  入れること。

# 出力形式
{output_format_instruction}

余計な前置き（「以下が記事です」等）は不要です。指定した出力形式のみを出力してください。
"""

    with st.spinner("記事を生成しています..."):
        try:
            result = generate(prompt, temperature=0.8)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    show_result(result, filename="blog_post.md")
