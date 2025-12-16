import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager


def _save_scene_text(scene_id: str):
    """씬 텍스트 저장 콜백 함수"""
    # 세션 상태에서 텍스트 값 가져오기
    textarea_key = f"type1_textarea_{scene_id}"
    if textarea_key in st.session_state:
        new_text = st.session_state[textarea_key]
        # JSON에 저장
        if video_manager.update_scene_field(scene_id, "text", new_text):
            st.success("✅ 저장되었습니다!")


def render_type1(scene: Dict[str, Any]):
    """
    Type 1 씬의 UI를 렌더링하는 함수
    텍스트 영역만 표시하고, 변경 시 자동으로 JSON에 저장됩니다.
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id, text, type 포함)
    """
    scene_id = scene.get('id')
    current_text = scene.get('text', '')
    
    # 텍스트 영역 - on_change 콜백으로 자동 저장
    st.text_area(
        "텍스트 입력",
        value=current_text,
        key=f"type1_textarea_{scene_id}",
        help="텍스트를 입력하세요. 변경 시 자동으로 저장됩니다.",
        height=100,
        on_change=_save_scene_text,
        args=(scene_id,)  # 콜백 함수에 scene_id 전달
    )

