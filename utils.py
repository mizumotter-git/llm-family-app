"""
画面表示以外の様々な関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
from dotenv import load_dotenv
import constants as ct
from duckduckgo_search import DDGS

############################################################
# 設定関連
############################################################
# 「.env」ファイルで定義した環境変数の読み込み
load_dotenv()


############################################################
# 関数定義
############################################################
# utils.py
import streamlit as st

def build_messages_for_openai(system_prompt: str, family_info_text: str, history: list, web_results: str = ""):
    context_text = system_prompt + family_info_text
    if web_results:
        context_text += "\n\n## 参考情報（Web検索結果）\n" + web_results

    messages = [{"role": "system", "content": context_text}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    return messages

def call_openai(client, messages, model=ct.MODEL, temperature=ct.TEMPERATURE):
    """
    OpenAIの呼び出し (簡易ラッパー)
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise

def search_web(query: str, max_results: int = 5) -> str:
    """
    DuckDuckGoでWeb検索し、上位結果をテキストで返す
    """
    try:
        results_text = ""
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                title = r.get("title", "")
                body = r.get("body", "")
                link = r.get("href", "")
                results_text += f"- {title}\n  {body}\n  {link}\n\n"
        return results_text.strip()
    except Exception as e:
        return f"(Web検索エラー: {e})"