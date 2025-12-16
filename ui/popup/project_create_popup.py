import streamlit as st
from project_manager import project_manager

@st.dialog("프로젝트 생성")
def create_dialog():
    # 다이얼로그마다 고유한 키 사용
    dialog_key = f"project_input_{st.session_state.get('dialog_id', 0)}"
    
    st.write("생성할 프로젝트의 이름을 입력하세요")
    name = st.text_input("프로젝트 이름", placeholder="예: 영상 편집 프로젝트", key=dialog_key)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("취소", use_container_width=True):
            # 다이얼로그 ID 변경으로 새로운 입력 필드 생성
            st.session_state.dialog_id = st.session_state.get('dialog_id', 0) + 1
            st.rerun()
    
    with col2:
        if st.button("생성", type="primary", use_container_width=True):
            if name and name.strip():
                result = project_manager.create_project(name.strip())
                
                if result["success"]:
                    st.success(result["message"])
                    st.session_state["last_created_project"] = result
                    st.session_state["show_success"] = True
                    # 다이얼로그 ID 변경으로 새로운 입력 필드 생성
                    st.session_state.dialog_id = st.session_state.get('dialog_id', 0) + 1
                    st.rerun()
                else:
                    st.error(result["message"])
            else:
                st.error("프로젝트 이름을 입력해주세요.")
