import streamlit as st
import shutil
from typing import Dict, Any, Optional
from service.video_manager import video_manager
from project_manager import project_manager
from pathlib import Path
from service.tts_service import TTSRequest, tts_service

subfolder = "audio"


def _save_audio_to_project(
    scene_id: str,
    field: str,
    source_file: Any,
    file_extension: str = None
) -> bool:
    """
    오디오 파일을 프로젝트의 audio 폴더에 저장하고 scene field에 경로를 저장하는 공통 함수
    
    Args:
        scene_id (str): 씬 ID
        field (str): 필드명
        source_file (Path): 저장할 소스 파일 경로 (Path 객체 또는 UploadedFile)
        file_extension (str, optional): 파일 확장자 (없으면 source_file에서 추출)
    
    Returns:
        bool: 성공 여부
    """
    try:
        # 프로젝트 경로 가져오기
        project_path = project_manager.get_project_path()
        if not project_path:
            st.error("프로젝트가 로드되지 않았습니다.")
            return False
        
        # audio 폴더 경로
        audio_folder = project_path / subfolder
        audio_folder.mkdir(parents=True, exist_ok=True)
        
        # 파일 확장자 추출
        if file_extension is None:
            if isinstance(source_file, Path):
                file_extension = source_file.suffix
            else:
                # UploadedFile인 경우
                file_extension = Path(source_file.name).suffix
        
        # 파일명 생성 (scene_id와 field를 포함)
        audio_filename = f"{scene_id}_{field}{file_extension}"
        target_path = audio_folder / audio_filename
        
        # 파일 저장/복사
        if isinstance(source_file, Path):
            # Path 객체인 경우 (TTS 생성 파일)
            shutil.copy2(source_file, target_path)
        else:
            # UploadedFile인 경우
            with open(target_path, "wb") as f:
                f.write(source_file.getbuffer())
        
        # 상대 경로 생성
        relative_path = f"{subfolder}/{audio_filename}"
        
        # scene field에 경로 저장
        if video_manager.update_scene_field(scene_id, field, relative_path):
            return True
        else:
            st.error("오디오 경로 저장에 실패했습니다.")
            return False
            
    except Exception as e:
        st.error(f"오디오 저장 중 오류가 발생했습니다: {e}")
        print(f"[AUDIO] 저장 오류: {e}")
        return False


def render_audio_input(scene: Dict[str, Any], field: str = "audio", tts_request: Optional[TTSRequest] = None):
    """
    오디오 업로드 및 재생 컴포넌트
    - field 값 없으면 uploader
    - field 값 있으면 audio + 삭제(❌)
    - 상단에 field 텍스트 출력
    """
    scene_id = scene.get("id")

    uploader_key = f"audio_{scene_id}_{field}"
    delete_key = f"delete_audio_{scene_id}_{field}"
    auto_key = f"auto_{scene_id}_{field}"

    # ✅ 상단 field 텍스트와 auto 버튼을 나란히 배치
    col_field, col_auto = st.columns([2, 1])
    
    with col_field:
        st.text(field)
    
    with col_auto:
        # tts_request가 있을 때만 auto 버튼 표시
        if tts_request:
            if st.button("auto", key=auto_key, help="자동 생성 (TTS)"):
                try:
                    # TTS 서비스 호출하여 음성 파일 생성
                    generated_file = tts_service.generate(tts_request)
                    
                    if generated_file and generated_file.exists():
                        # 공통 함수를 사용하여 프로젝트에 저장
                        if _save_audio_to_project(scene_id, field, generated_file):
                            st.success("TTS로 오디오가 생성되었습니다!")
                            st.rerun()
                    else:
                        st.error("TTS 생성에 실패했습니다.")
                        
                except Exception as e:
                    st.error(f"TTS 생성 중 오류가 발생했습니다: {str(e)}")
                    print(f"[AUTO] TTS 생성 오류: {e}")

    def _save_scene_audio():
        """파일 업로드 시 1회 실행 -> 저장 -> scene field에 경로 저장"""
        if uploader_key in st.session_state and st.session_state[uploader_key] is not None:
            uploaded_file = st.session_state[uploader_key]
            # 공통 함수를 사용하여 프로젝트에 저장
            _save_audio_to_project(scene_id, field, uploaded_file)

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
        if st.button("X", key=delete_key, help="오디오 제거"):
            video_manager.update_scene_field(scene_id, field, None)

            # 선택: uploader state도 비워주기
            if uploader_key in st.session_state:
                st.session_state[uploader_key] = None

            st.rerun()