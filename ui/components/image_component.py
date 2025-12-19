import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager
from project_manager import project_manager
from PIL import Image
from pathlib import Path

subfolder = "image"

def render_image_input(scene: Dict[str, Any], field: str = "image"):
    scene_id = scene.get("id")

    uploader_key = f"image_{scene_id}_{field}"
    delete_key = f"delete_{scene_id}_{field}"

    def _save_scene_image():
        """파일 업로드 시 1회 실행 -> 프로젝트 폴더 저장 -> scene field에 경로 저장"""
        if uploader_key in st.session_state and st.session_state[uploader_key] is not None:
            uploaded_file = st.session_state[uploader_key]
            try:
                file_extension = Path(uploaded_file.name).suffix
                image_filename = f"{scene_id}_{field}{file_extension}"

                relative_path = project_manager.save_image_file(
                    uploaded_file, image_filename, subfolder
                )

                if relative_path:
                    video_manager.update_scene_field(scene_id, field, relative_path)

            except Exception as e:
                st.error(f"이미지 저장 중 오류가 발생했습니다: {e}")

    # 저장된 이미지 경로
    saved_image_path = video_manager.get_scene_field(scene_id, field, None)

    # ✅ 저장된 이미지가 없으면: 업로더만 보여주기
    if not saved_image_path:
        st.file_uploader(
            label=field,
            type=["png", "jpg", "jpeg", "gif", "webp"],
            key=uploader_key,
            help="이미지 파일을 업로드하면 저장됩니다.",
            on_change=_save_scene_image,
        )
        return

    # ✅ 저장된 이미지가 있으면: 미리보기 + 삭제(❌)
    col1, col2 = st.columns([6, 1])

    with col1:
        try:
            full_image_path = project_manager.get_image_path(saved_image_path)

            if full_image_path and full_image_path.exists():
                image = Image.open(full_image_path)
                st.image(image, width="content")

                # 미리보기 높이 제한(원본은 그대로)
                st.markdown(
                    """
                    <style>
                    .stImage img {
                        max-height: 80px !important;
                        width: auto !important;
                        object-fit: contain !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.warning(f"이미지 파일을 찾을 수 없습니다: {saved_image_path}")

        except Exception as e:
            st.error(f"이미지를 불러오는 중 오류가 발생했습니다: {e}")

    with col2:
        # ❌ 버튼(텍스트로 X)
        if st.button("X", key=delete_key, help="이미지 제거"):
            video_manager.update_scene_field(scene_id, field, None)

            # 업로더가 바로 보이도록(선택)
            if uploader_key in st.session_state:
                st.session_state[uploader_key] = None

            st.rerun()