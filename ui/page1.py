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
        for idx, scene in enumerate(scenes, 1):
            scene_type = scene.get('type', 'type1')
            scene_id = scene.get('id')
            
            # 씬 헤더와 삭제 버튼을 나란히 배치
            col_header, col_delete = st.columns([10, 1])
            
            with col_header:
                # 씬 헤더 표시
                st.markdown(f"### 씬 {idx} (Type: {scene_type})")
            
            with col_delete:
                # 삭제 버튼 (X 표시)
                if st.button("❌", key=f"delete_{scene_id}", help="씬 삭제"):
                    if video_manager.remove_scene(scene_id):
                        st.success("씬이 삭제되었습니다.")
                        st.rerun()
                    else:
                        st.error("씬 삭제에 실패했습니다.")
            
            # 씬 타입에 따라 해당하는 UI 렌더링 함수 호출
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
            
            # 씬 사이 구분선 (마지막 씬이 아니면)
            if idx < len(scenes):
                st.divider()
    else:
        st.info("추가된 씬이 없습니다. + 버튼을 눌러 씬을 추가하세요.")
    
