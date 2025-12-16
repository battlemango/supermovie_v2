import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager
from PIL import Image
import io


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
    텍스트 영역과 이미지 업로드 기능을 제공합니다.
    
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
    
    # 이미지 업로드 영역과 이미지 표시를 나란히 배치
    col1, col2 = st.columns(2)
    
    with col1:
        # 이미지 업로드 영역 (라벨 숨김)
        uploaded_file = st.file_uploader(
            "이미지를 드래그하거나 클릭하여 업로드하세요",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            key=f"type1_image_{scene_id}",
            label_visibility="hidden",  # 라벨 숨기기
            help="이미지 파일을 업로드하면 여기에 표시됩니다."
        )
    
    with col2:
        # 업로드된 이미지가 있으면 표시
        if uploaded_file is not None:
            try:
                # 이미지 읽기 (원본 그대로)
                image = Image.open(uploaded_file)
                
                # 이미지 표시 (높이만 70px로 제한, 비율 유지, 원본 이미지는 그대로)
                st.image(
                    image,
                    width=None,
                    use_container_width=False
                )
                # CSS로 이미지 높이만 제한 (원본 이미지는 리사이즈하지 않음, 비율 유지)
                st.markdown(
                    """
                    <style>
                    .stImage img {
                        max-height: 100px !important;
                        width: auto !important;
                        object-fit: contain !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"이미지를 불러오는 중 오류가 발생했습니다: {e}")
        else:
            # 이미지가 없을 때 빈 공간 표시
            st.write("")

