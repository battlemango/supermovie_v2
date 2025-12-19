import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager


def render_text_input(
    scene: Dict[str, Any],
    field: str,
    height: int = 50,
    label: str = None,
    multiline: bool = True,   # ✅ 추가: True면 text_area, False면 text_input(한줄)
):
    """
    텍스트 입력 컴포넌트 - 여러 타입에서 공용으로 사용 가능

    Args:
        scene (dict): 씬 정보 딕셔너리 (id 포함)
        field (str): 저장할 필드명
        height (int): text_area 높이 (multiline=True일 때만 사용)
        label (str, optional): 라벨 텍스트 (None이면 field 사용)
        multiline (bool): True=여러줄(text_area), False=한줄(text_input)
    """
    scene_id = scene.get("id")
    current_value = scene.get(field, "")

    key = f"text_{scene_id}_{field}"

    if label is None:
        label = field

    def _save_text():
        if key in st.session_state:
            new_text = st.session_state[key]
            if video_manager.update_scene_field(scene_id, field, new_text) is False:
                st.error("저장에 실패했습니다.")

    if multiline:
        st.text_area(
            label,
            value=current_value,
            key=key,
            help=f"{label}을(를) 입력하세요. 변경 시 자동으로 저장됩니다.",
            height=height,
            on_change=_save_text,
        )
    else:
        st.text_input(
            label,
            value=current_value,
            key=key,
            help=f"{label}을(를) 입력하세요. 변경 시 자동으로 저장됩니다.",
            on_change=_save_text,
        )