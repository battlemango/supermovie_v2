import streamlit as st
from service.video_manager import video_manager

@st.dialog("씬 타입 선택")
def scene_type_dialog():
    """씬 타입을 선택하는 팝업 다이얼로그"""
    st.write("씬의 타입을 선택하세요")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Type 1", use_container_width=True, type="primary"):
            # type1으로 씬 추가
            new_scene = video_manager.add_scene(scene_type="type1")
            if new_scene:
                st.success(f"씬이 추가되었습니다! (Type: type1)")
                st.rerun()
            else:
                st.error("프로젝트를 먼저 로드해주세요.")
    
    with col2:
        if st.button("Type 2", use_container_width=True, type="primary"):
            # type2로 씬 추가
            new_scene = video_manager.add_scene(scene_type="type2")
            if new_scene:
                st.success(f"씬이 추가되었습니다! (Type: type2)")
                st.rerun()
            else:
                st.error("프로젝트를 먼저 로드해주세요.")
    
    with col3:
        if st.button("Type 3", use_container_width=True, type="primary"):
            # type3으로 씬 추가
            new_scene = video_manager.add_scene(scene_type="type3")
            if new_scene:
                st.success(f"씬이 추가되었습니다! (Type: type3)")
                st.rerun()
            else:
                st.error("프로젝트를 먼저 로드해주세요.")
    
    # 닫기 버튼
    st.divider()
    if st.button("취소", use_container_width=True):
        st.rerun()

def show():
    
    # + 버튼으로 씬 추가
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕", use_container_width=True, help="새 씬 추가"):
            # 팝업 다이얼로그 열기
            scene_type_dialog()
    
    # 현재 씬 목록 표시
    video_data = video_manager.get_video_data()
    scenes = video_data.get("scenes", [])
    
    if scenes:
        st.subheader("📹 씬 목록")
        for idx, scene in enumerate(scenes, 1):
            scene_type = scene.get('type', 'N/A')
            scene_text = scene.get('text', 'N/A')
            scene_id = scene.get('id', 'N/A')[:8] if scene.get('id') else 'N/A'
            st.write(f"{idx}. {scene_text} | Type: {scene_type} | ID: {scene_id}...")
    else:
        st.info("추가된 씬이 없습니다. + 버튼을 눌러 씬을 추가하세요.")
    
