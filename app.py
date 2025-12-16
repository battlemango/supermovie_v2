import streamlit as st
from project_manager import project_manager
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

# 사이드바
st.sidebar.header("🎬 Streamlit 앱")


current_project = project_manager.get_current_project()
if current_project:
    st.sidebar.subheader(f"{current_project['folder_name']}")

    
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("📝 Create", use_container_width=True):
        create_dialog()

with col2:
    if st.button("📁 Load", use_container_width=True):
        load_dialog()

# 구분선
st.sidebar.divider()


if st.sidebar.button("페이지 1", use_container_width=True, key="page1_btn"):
    st.session_state.current_page = 'page1'

if st.sidebar.button("페이지 2", use_container_width=True, key="page2_btn"):
    st.session_state.current_page = 'page2'

if st.sidebar.button("페이지 3", use_container_width=True, key="page3_btn"):
    st.session_state.current_page = 'page3'



# 구분선
st.divider()


# 페이지 렌더링
if st.session_state.current_page == 'page1':
    page1.show()
elif st.session_state.current_page == 'page2':
    page2.show()
elif st.session_state.current_page == 'page3':
    page3.show()

# 푸터
st.divider()
st.markdown("---")
st.markdown("*Made with ❤️ using Streamlit*")
