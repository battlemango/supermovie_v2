import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager
from project_manager import project_manager
from PIL import Image
from pathlib import Path

subfolder = "image"

def render_image_input(scene: Dict[str, Any], field: str = "image"):
    """
    이미지 업로드 및 표시 컴포넌트 - 여러 타입에서 공용으로 사용 가능
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id 포함)
        field (str): 저장할 필드명 (기본값: "image")
        subfolder (str): 이미지를 저장할 하위 폴더명 (기본값: "image")
    """
    scene_id = scene.get('id')
    
    # 이미지 저장 콜백 함수
    def _save_scene_image():
        """씬 이미지 저장 콜백 함수 - 파일이 업로드될 때만 실행됨"""
        uploader_key = f"image_{scene_id}_{field}"
        if uploader_key in st.session_state and st.session_state[uploader_key] is not None:
            uploaded_file = st.session_state[uploader_key]
            
            try:
                # 파일명 생성 (씬 ID + 확장자)
                file_extension = Path(uploaded_file.name).suffix
                image_filename = f"{scene_id}_{field}{file_extension}"
                
                # project_manager를 통해 이미지 저장
                relative_path = project_manager.save_image_file(uploaded_file, image_filename, subfolder)
                
                if relative_path:
                    # 씬에 이미지 경로 저장
                    if video_manager.update_scene_field(scene_id, field, relative_path):
                        st.rerun()
            except Exception as e:
                st.error(f"이미지 저장 중 오류가 발생했습니다: {e}")
    
    # 이미지 업로드 영역과 이미지 표시를 나란히 배치
    col1, col2 = st.columns(2)
    
    with col1:
        # 이미지 업로드 영역 (라벨 숨김) - on_change로 업로드 시 한 번만 저장
        uploaded_file = st.file_uploader(
            "이미지를 드래그하거나 클릭하여 업로드하세요",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            key=f"image_{scene_id}_{field}",
            label_visibility="hidden",  # 라벨 숨기기
            help="이미지 파일을 업로드하면 여기에 표시됩니다.",
            on_change=_save_scene_image  # 파일 업로드 시 한 번만 실행
        )
    
    with col2:
        # 저장된 이미지 경로 가져오기
        saved_image_path = video_manager.get_scene_field(scene_id, field, None)
        
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
                        width='content',
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

