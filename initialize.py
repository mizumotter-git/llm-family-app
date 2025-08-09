"""
最初の画面読み込み時にのみ実行される初期化処理が記述されたファイルです。
"""
############################################################
# ライブラリの読み込み
############################################################
from dotenv import load_dotenv

############################################################
# 設定関連
############################################################
# 「.env」ファイルで定義した環境変数の読み込み
load_dotenv()


############################################################
# 関数定義
############################################################
import os
from dotenv import load_dotenv
import streamlit as st
import openai

def init_app():
    """
    初期化処理:
    - OpenAIクライアントを作成して返す
    - session_state の初期値を設定する
    """
    load_dotenv()

    # 1) .env
    api_key = os.getenv("OPENAI_API_KEY")

    # 2) st.secrets
    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        st.warning("サイドバーでOpenAI APIキーを入力するか、.envファイルに設定してください。")
        st.stop()

    # OpenAIクライアント作成
    client = openai.OpenAI(api_key=api_key)

    # session_state の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "family_members" not in st.session_state:
        st.session_state.family_members = [
            {"relationship": "本人", "age": 45},
            {"relationship": "配偶者", "age": 45},
        ]

    return client
