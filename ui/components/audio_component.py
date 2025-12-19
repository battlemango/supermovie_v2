import streamlit as st
from typing import Dict, Any
from service.video_manager import video_manager
from project_manager import project_manager
from pathlib import Path

subfolder = "audio"

def render_audio_input(scene: Dict[str, Any], field: str = "audio"):
    """
    오디오 업로드 및 재생 컴포넌트
    - field 값 없으면 uploader
    - field 값 있으면 audio + 삭제(❌)
    - 상단에 field 텍스트 출력
    """
    scene_id = scene.get("id")

    uploader_key = f"audio_{scene_id}_{field}"
    delete_key = f"delete_audio_{scene_id}_{field}"

    # ✅ 상단 field 텍스트
    st.text(field)

    def _save_scene_audio():
        """파일 업로드 시 1회 실행 -> 저장 -> scene field에 경로 저장"""
        if uploader_key in st.session_state and st.session_state[uploader_key] is not None:
            uploaded_file = st.session_state[uploader_key]
            try:
                file_extension = Path(uploaded_file.name).suffix
                audio_filename = f"{scene_id}_{field}{file_extension}"

                relative_path = project_manager.save_audio_file(
                    uploaded_file,
                    audio_filename,
                    subfolder
                )

                if relative_path:
                    video_manager.update_scene_field(scene_id, field, relative_path)

            except Exception as e:
                st.error(f"오디오 저장 중 오류가 발생했습니다: {e}")

    saved_audio_path = video_manager.get_scene_field(scene_id, field, None)

    # ✅ 없으면: 업로더만
    if not saved_audio_path:
        st.file_uploader(
            "오디오 파일 업로드",
            type=["mp3", "wav", "m4a", "aac", "ogg", "flac"],
            key=uploader_key,
            label_visibility="collapsed",
            help="오디오 파일을 업로드하면 저장됩니다.",
            on_change=_save_scene_audio
        )
        return

    # ✅ 있으면: audio + ❌ (옆 배치하려면 columns가 정석)
    col_audio, col_btn = st.columns([3, 1], vertical_alignment="center")

    with col_audio:
        try:
            full_audio_path = project_manager.get_relative_path(saved_audio_path)
            if full_audio_path and full_audio_path.exists():
                st.audio(str(full_audio_path))
            elif full_audio_path:
                st.warning(f"오디오 파일을 찾을 수 없습니다: {saved_audio_path}")
        except Exception as e:
            st.error(f"오디오를 불러오는 중 오류가 발생했습니다: {e}")

    with col_btn:
        if st.button("❌", key=delete_key, help="오디오 제거"):
            video_manager.update_scene_field(scene_id, field, None)

            # 선택: uploader state도 비워주기
            if uploader_key in st.session_state:
                st.session_state[uploader_key] = None

            st.rerun()