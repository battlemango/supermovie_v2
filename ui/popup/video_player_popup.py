import streamlit as st
from pathlib import Path


@st.dialog("비디오 재생")
def video_player_dialog(video_path: Path, scene_title: str = "비디오"):
    """
    비디오 재생 팝업 다이얼로그
    
    Args:
        video_path (Path): 재생할 비디오 파일 경로
        scene_title (str): 씬 제목 (기본값: "비디오")
    """
    # 씬 제목 표시
    st.markdown(f"### {scene_title}")
    
    # 비디오 파일 존재 여부 확인
    if not video_path or not video_path.exists():
        st.error("비디오 파일을 찾을 수 없습니다.")
        st.info(f"경로: {video_path}")
        return
    
    # 비디오 파일 정보 표시
    file_size = video_path.stat().st_size / (1024 * 1024)  # MB 단위
    st.caption(f"파일 크기: {file_size:.2f} MB")
    
    # 비디오 재생
    st.video(str(video_path))
    
    # 닫기 버튼
    if st.button("닫기", type="primary", width="stretch"):
        st.rerun()

