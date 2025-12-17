import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager


def render_text_input(scene: Dict[str, Any], field: str, height: int = 50, label: str = None):
    """
    텍스트 입력 컴포넌트 - 여러 타입에서 공용으로 사용 가능
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id 포함)
        field (str): 저장할 필드명 (예: "text", "title", "description" 등)
        height (int): 텍스트 영역 높이 (기본값: 100)
        label (str, optional): 라벨 텍스트 (None이면 field를 사용)
    """
    scene_id = scene.get('id')
    # scene에서 field 값 가져오기
    current_value = scene.get(field, '')
    
    # key는 자동 생성 (scene_id와 field 조합)
    textarea_key = f"text_{scene_id}_{field}"
    
    # 라벨이 없으면 field를 사용
    if label is None:
        label = field
    
    # 저장 콜백 함수
    def _save_text():
        """텍스트 저장 콜백 함수"""
        if textarea_key in st.session_state:
            new_text = st.session_state[textarea_key]
            # JSON에 저장
            if video_manager.update_scene_field(scene_id, field, new_text) == False:
                st.error("저장에 실패했습니다.")
    
    # 텍스트 영역 - on_change 콜백으로 자동 저장
    st.text_area(
        label,
        value=current_value,
        key=textarea_key,
        help=f"{label}을(를) 입력하세요. 변경 시 자동으로 저장됩니다.",
        height=height,
        on_change=_save_text
    )

