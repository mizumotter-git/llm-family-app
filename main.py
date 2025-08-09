"""
Webアプリのメイン処理が記述されたファイルです。
"""
############################################################
# 1. ライブラリの読み込み
############################################################
from initialize import init_app
import utils
import constants as ct
import components as cn
import streamlit as st
import logging

############################################################
# 2. 設定関連
############################################################
# ログ出力を行うためのロガーの設定
logger = logging.getLogger(ct.LOGGER_NAME)

############################################################
# 3. 初期化処理
############################################################
try:
    # 初期化処理（「initialize.py」の「init_app」関数を実行）
    init_app()
except Exception as e:
    # エラーログの出力
    logger.error(f"{ct.INITIALIZE_ERROR_MESSAGE}\n{e}")
    # エラーメッセージの画面表示
    st.error(utils.build_error_message(ct.INITIALIZE_ERROR_MESSAGE), icon=ct.ERROR_ICON)
    # 後続の処理を中断
    st.stop()

# アプリ起動時のログファイルへの出力
if not "init_app" in st.session_state:
    st.session_state.init_app = True
    logger.info(ct.APP_BOOT_MESSAGE)



# --- ページ設定 ---
st.set_page_config(page_title=ct.PAGE_TITLE, page_icon=ct.PAGE_ICON, layout=ct.LAYOUT)

# 初期化処理（APIキー取得・client作成・session_state初期化）
client = init_app()

# サイドバー（家族構成）を表示し、family_info_text 検索設定を取得
family_info_text, use_web = cn.render_sidebar_family()

# メイン表示
cn.render_title_and_caption()

# セッションステート messages が init_app でセットされているはず
if "messages" not in st.session_state:
    st.session_state.messages = []

cn.render_messages()

# ユーザー入力
if prompt := st.chat_input(ct.CHAT_INPUT_HELPER_TEXT):
    # ユーザーのメッセージを履歴に追加して表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    web_results = ""
    if use_web:
        with st.spinner("Web検索中..."):
            web_results = utils.search_web(prompt, max_results=5)

    # アシスタントの応答を生成
    with st.chat_message("assistant"):
        with st.spinner(ct.SPINNER):
            try:
                messages_for_openai = utils.build_messages_for_openai(ct.SYSTEM_PROMPT, family_info_text, st.session_state.messages)
                full_response = utils.call_openai(
                        client,
                        messages_for_openai,
                        model = ct.MODEL,
                        temperature = ct.TEMPERATURE)

                # 応答を表示
                st.markdown(full_response)

                # 履歴へ追加
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
                # エラー発生時は最後のユーザーメッセージを履歴から削除
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()
