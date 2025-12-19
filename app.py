import streamlit as st
from project_manager import project_manager
from settings import Settings
from ui import page1, page2, page3
from ui.popup.project_create_popup import create_dialog
from ui.popup.project_load_popup import load_dialog

# 페이지 설정
st.set_page_config(
    page_title="간단한 Streamlit 앱",
    page_icon="🎬",
    layout="centered"
)

# 세션 상태 초기화
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'page1'

# Settings에서 debug_mode 값을 가져와서 세션 상태 초기화
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = Settings.is_debug_mode()

# 사이드바
st.sidebar.header("🎬 Streamlit 앱")


current_project = project_manager.get_current_project()
if current_project:
    st.sidebar.subheader(f"{current_project['folder_name']}")

    
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("📝 Create", width="stretch"):
        create_dialog()

with col2:
    if st.button("📁 Load", width="stretch"):
        load_dialog()

# Debug toggle 버튼
debug_enabled = st.sidebar.toggle("🐛 Debug Mode", key="debug_toggle", value=st.session_state.debug_mode)
# 토글 상태가 변경되면 세션 상태와 Settings 업데이트
if debug_enabled != st.session_state.debug_mode:
    st.session_state.debug_mode = debug_enabled
    Settings.set_debug_mode(debug_enabled)

# 구분선
st.sidebar.divider()


if st.sidebar.button("페이지 1", width="stretch", key="page1_btn"):
    st.session_state.current_page = 'page1'

if st.sidebar.button("페이지 2", width="stretch", key="page2_btn"):
    st.session_state.current_page = 'page2'

if st.sidebar.button("페이지 3", width="stretch", key="page3_btn"):
    st.session_state.current_page = 'page3'





# 페이지 렌더링
if st.session_state.current_page == 'page1':
    page1.show()
elif st.session_state.current_page == 'page2':
    page2.show()
elif st.session_state.current_page == 'page3':
    page3.show()
