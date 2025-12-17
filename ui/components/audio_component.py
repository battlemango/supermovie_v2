import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager
from project_manager import project_manager
from pathlib import Path

subfolder = "audio"

def render_audio_input(scene: Dict[str, Any], field: str = "audio"):
    """
    오디오 업로드 및 재생 컴포넌트 - 여러 타입에서 공용으로 사용 가능

    Args:
        scene (dict): 씬 정보 딕셔너리 (id 포함)
        field (str): 저장할 필드명 (기본값: "audio")
    """
    scene_id = scene.get("id")

    def _save_scene_audio():
        """씬 오디오 저장 콜백 함수 - 파일이 업로드될 때만 실행됨"""
        uploader_key = f"audio_{scene_id}_{field}"
        if uploader_key in st.session_state and st.session_state[uploader_key] is not None:
            uploaded_file = st.session_state[uploader_key]

            try:
                # 파일명 생성 (씬 ID + 확장자)
                file_extension = Path(uploaded_file.name).suffix
                audio_filename = f"{scene_id}_{field}{file_extension}"

                # project_manager를 통해 오디오 저장
                relative_path = project_manager.save_audio_file(
                    uploaded_file,
                    audio_filename,
                    subfolder
                )

                if relative_path:
                    # 씬에 오디오 경로 저장
                    if video_manager.update_scene_field(scene_id, field, relative_path):
                        st.rerun()

            except Exception as e:
                st.error(f"오디오 저장 중 오류가 발생했습니다: {e}")

    col1, col2 = st.columns(2)

    with col1:
        st.file_uploader(
            "오디오 파일을 드래그하거나 클릭하여 업로드하세요",
            type=["mp3", "wav", "m4a", "aac", "ogg", "flac"],
            key=f"audio_{scene_id}_{field}",
            label_visibility="hidden",
            help="오디오 파일을 업로드하면 오른쪽에서 재생할 수 있습니다.",
            on_change=_save_scene_audio
        )

    with col2:
        saved_audio_path = video_manager.get_scene_field(scene_id, field, None)

        if saved_audio_path:
            try:
                full_audio_path = project_manager.get_audio_path(saved_audio_path)

                if full_audio_path and full_audio_path.exists():
                    # Streamlit 오디오 플레이어
                    st.audio(str(full_audio_path))
                    # 경로도 보고 싶으면(선택)
                    # st.caption(saved_audio_path)
                elif full_audio_path:
                    st.warning(f"오디오 파일을 찾을 수 없습니다: {saved_audio_path}")
            except Exception as e:
                st.error(f"오디오를 불러오는 중 오류가 발생했습니다: {e}")
        else:
            st.write("")