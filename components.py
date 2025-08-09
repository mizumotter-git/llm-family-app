"""
画面表示に特化した関数定義のファイルです。
"""
############################################################
# ライブラリの読み込み
############################################################
import streamlit as st
import constants as ct


############################################################
# 関数定義
############################################################
def render_sidebar_family():
    """
    サイドバーで家族構成を入力する UI を表示し、
    最終的に family_info_text を返す。
    """
    st.sidebar.header(ct.SIDEBAR_HEADER)
    st.sidebar.info(ct.SIDEBAR_INFO)

    def add_member():
        st.session_state.family_members.append({"relationship": "", "age": 10})

    def remove_member(index):
        if len(st.session_state.family_members) > 1:
            st.session_state.family_members.pop(index)

    for i, member in enumerate(st.session_state.family_members):
        cols = st.sidebar.columns([3, 2, 1])
        st.session_state.family_members[i]['relationship'] = cols[0].text_input(
            f"続柄 {i+1}", member['relationship'], key=f"rel_{i}"
        )
        st.session_state.family_members[i]['age'] = cols[1].number_input(
            f"年齢 {i+1}", min_value=0, max_value=120, value=member['age'], key=f"age_{i}"
        )
        if cols[2].button("ー", key=f"del_{i}", help="このメンバーを削除"):
            remove_member(i)
            st.rerun()

    st.sidebar.button("＋ メンバーを追加", on_click=add_member)

    st.sidebar.divider()
    # ここから検索
    st.sidebar.header("🔍 検索設定")
    use_web = st.sidebar.checkbox("Web検索を有効にする", value=False)

    # family_info_text を作成して返す
    family_info_text = "\n## 家族構成\n"
    for member in st.session_state.family_members:
        if member.get('relationship') and member.get('age') is not None:
            family_info_text += f"- {member['relationship']}: {member['age']}歳\n"

    return family_info_text, use_web

def render_title_and_caption():
    st.title(ct.PAGE_TITLE)
    st.caption(ct.CAPTION)

def render_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
