import streamlit as st
from service.video_manager import video_manager
from ui.scene_types import render_type1, render_type2, render_type3

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
            scene_type = scene.get('type', 'type1')
            
            # 씬 타입에 따라 해당하는 UI 렌더링 함수 호출
            with st.expander(f"씬 {idx}: {scene.get('text', 'N/A')} (Type: {scene_type})", expanded=False):
                if scene_type == "type1":
                    render_type1(scene)
                elif scene_type == "type2":
                    render_type2(scene)
                elif scene_type == "type3":
                    render_type3(scene)
                else:
                    # 알 수 없는 타입인 경우 기본 UI 표시
                    st.warning(f"알 수 없는 씬 타입: {scene_type}")
                    st.json(scene)
    else:
        st.info("추가된 씬이 없습니다. + 버튼을 눌러 씬을 추가하세요.")
    
