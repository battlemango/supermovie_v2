import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager
from project_manager import project_manager
from PIL import Image
from pathlib import Path
from ui.components.text_component import render_text_input


def _save_scene_image(scene_id: str):
    """씬 이미지 저장 콜백 함수 - 파일이 업로드될 때만 실행됨"""
    # 세션 상태에서 업로드된 파일 가져오기
    uploader_key = f"type1_image_{scene_id}"
    if uploader_key in st.session_state and st.session_state[uploader_key] is not None:
        uploaded_file = st.session_state[uploader_key]
        
        try:
            # 파일명 생성 (씬 ID + 확장자)
            file_extension = Path(uploaded_file.name).suffix
            image_filename = f"{scene_id}{file_extension}"
            
            # project_manager를 통해 이미지 저장
            relative_path = project_manager.save_image_file(uploaded_file, image_filename, "image")
            
            if relative_path:
                # 씬에 이미지 경로 저장
                if video_manager.update_scene_field(scene_id, "image", relative_path):
                    st.rerun()
        except Exception as e:
            st.error(f"이미지 저장 중 오류가 발생했습니다: {e}")


def render_type1(scene: Dict[str, Any]):
    """
    Type 1 씬의 UI를 렌더링하는 함수
    텍스트 영역과 이미지 업로드 기능을 제공합니다.
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id, text, type 포함)
    """
    scene_id = scene.get('id')
    
    # 텍스트 입력 컴포넌트 사용
    render_text_input(scene, "text", height=100, label="텍스트1")
    render_text_input(scene, "text2", height=100, label="텍스트2")
    
    # 이미지 업로드 영역과 이미지 표시를 나란히 배치
    col1, col2 = st.columns(2)
    
    with col1:
        # 이미지 업로드 영역 (라벨 숨김) - on_change로 업로드 시 한 번만 저장
        uploaded_file = st.file_uploader(
            "이미지를 드래그하거나 클릭하여 업로드하세요",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            key=f"type1_image_{scene_id}",
            label_visibility="hidden",  # 라벨 숨기기
            help="이미지 파일을 업로드하면 여기에 표시됩니다.",
            on_change=_save_scene_image,  # 파일 업로드 시 한 번만 실행
            args=(scene_id,)  # 콜백 함수에 scene_id 전달
        )
    
    with col2:
        # 저장된 이미지 경로 가져오기
        saved_image_path = video_manager.get_scene_field(scene_id, "image", None)
        
        # 저장된 이미지가 있으면 표시
        if saved_image_path:
            try:
                # project_manager를 통해 이미지 경로 가져오기
                full_image_path = project_manager.get_image_path(saved_image_path)
                
                if full_image_path and full_image_path.exists():
                    # 이미지 읽기 및 표시
                    image = Image.open(full_image_path)
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
                elif full_image_path:
                    st.warning(f"이미지 파일을 찾을 수 없습니다: {saved_image_path}")
            except Exception as e:
                st.error(f"이미지를 불러오는 중 오류가 발생했습니다: {e}")
        else:
            # 이미지가 없을 때 빈 공간 표시
            st.write("")

