import streamlit as st
from project_manager import project_manager

@st.dialog("프로젝트 로드")
def load_dialog():
    st.write("로드할 프로젝트를 선택하세요")
    
    # 프로젝트 목록 가져오기
    projects = project_manager.get_projects_list()
    
    if not projects:
        st.warning("생성된 프로젝트가 없습니다.")
        if st.button("닫기", width="stretch"):
            st.rerun()
        return
    
    # 현재 선택된 프로젝트 표시
    current_project = project_manager.get_current_project()
    
    # 각 프로젝트를 클릭 가능한 버튼으로 표시
    for project in projects:
        # Project 객체는 딕셔너리처럼 접근 가능 (__getitem__ 구현)
        # 폴더 이름에서 타임스탬프와 프로젝트 이름 분리
        if "_" in project['folder_name']:
            timestamp, name = project['folder_name'].split("_", 1)
            # 타임스탬프를 읽기 쉬운 형식으로 변환
            try:
                dt = timestamp[:4] + "-" + timestamp[4:6] + "-" + timestamp[6:8] + " " + timestamp[9:11] + ":" + timestamp[11:13] + ":" + timestamp[13:15]
                display_name = f"{name} ({dt})"
            except:
                display_name = project['folder_name']
        else:
            display_name = project['folder_name']
        
        # 현재 선택된 프로젝트는 강조 표시
        if current_project and current_project['folder_name'] == project['folder_name']:
            button_type = "primary"
            emoji = "✅ "
        else:
            button_type = "secondary"
            emoji = "📁 "
        
        # 프로젝트 선택 버튼
        if st.button(f"{emoji}{display_name}", key=f"select_{project['folder_name']}", width="stretch", type=button_type):
            # 현재 프로젝트 업데이트 (Project 객체 전달)
            project_manager.load_project(project)
            st.success(f"✅ '{project['project_name']}' 프로젝트를 로드했습니다.")
            st.rerun()
    
    # 닫기 버튼
    st.divider()
    if st.button("닫기", width="stretch"):
        st.rerun()
