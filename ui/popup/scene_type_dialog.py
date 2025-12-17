import streamlit as st
from service.video_manager import video_manager
from ui.scene_types import scene_classes, get_scene_display_name


def get_available_scene_types():
    """
    ui/scene_types/__init__.py에 정의된 scene_classes에서 씬 타입 정보를 가져옴
    
    Returns:
        list: (scene_type_key, class_name, display_name) 튜플의 리스트
    """
    scene_types = []
    
    for scene_type_key, (scene_class, display_name) in scene_classes.items():
        class_name = scene_class.__name__
        scene_types.append((scene_type_key, class_name, display_name))
    
    return scene_types


@st.dialog("씬 타입 선택")
def scene_type_dialog():
    """씬 타입을 선택하는 팝업 다이얼로그"""
    st.write("씬의 타입을 선택하세요")
    
    # 동적으로 scene type 목록 가져오기
    scene_types = get_available_scene_types()
    
    if not scene_types:
        st.error("사용 가능한 씬 타입이 없습니다.")
        return
    
    # 3열 레이아웃으로 버튼 배치
    cols = st.columns(3)
    
    for i, (scene_type_key, class_name, display_name) in enumerate(scene_types):
        col = cols[i % 3]
        
        with col:
            if st.button(display_name, width="stretch", type="primary", key=f"btn_{scene_type_key}"):
                # 해당 타입으로 씬 추가
                new_scene = video_manager.add_scene(scene_type=scene_type_key)
                if new_scene:
                    st.success(f"씬이 추가되었습니다! (Type: {display_name})")
                    st.rerun()
                else:
                    st.error("프로젝트를 먼저 로드해주세요.")
    
    # 닫기 버튼
    st.divider()
    if st.button("취소", width="stretch"):
        st.rerun()
