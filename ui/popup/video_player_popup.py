import streamlit as st
from pathlib import Path
import base64


@st.dialog("비디오 재생")
def video_player_dialog(video_path: Path, scene_title: str = "비디오"):
    """
    비디오 재생 팝업 다이얼로그 (자동 재생)
    
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
    
    # 비디오 파일을 base64로 인코딩하여 자동 재생
    try:
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            video_base64 = base64.b64encode(video_bytes).decode()
            video_extension = video_path.suffix.lower()
            
            # MIME 타입 결정
            mime_type_map = {
                ".mp4": "video/mp4",
                ".webm": "video/webm",
                ".ogg": "video/ogg",
                ".ogv": "video/ogg"
            }
            mime_type = mime_type_map.get(video_extension, "video/mp4")
            
            # HTML5 video 태그로 자동 재생 (즉시 시작, 소리 있음)
            video_html = f"""
            <video width="100%" controls autoplay style="border-radius: 10px;">
                <source src="data:{mime_type};base64,{video_base64}" type="{mime_type}">
                Your browser does not support the video tag.
            </video>
            <script>
                (function() {{
                    var video = document.querySelector('video');
                    if (video) {{
                        // 음소거 해제하고 바로 재생
                        video.muted = false;
                        video.volume = 1.0;
                        
                        // 비디오가 로드되면 바로 재생
                        video.addEventListener('loadeddata', function() {{
                            video.play().catch(function(error) {{
                                console.log('Autoplay prevented:', error);
                                // 자동 재생 실패 시에도 음소거 해제 (사용자가 수동 재생 가능)
                                video.muted = false;
                            }});
                        }});
                        
                        // 이미 로드된 경우 즉시 재생
                        if (video.readyState >= 2) {{
                            video.play().catch(function(error) {{
                                console.log('Autoplay prevented:', error);
                                video.muted = false;
                            }});
                        }}
                    }}
                }})();
            </script>
            """
            st.markdown(video_html, unsafe_allow_html=True)
    except Exception as e:
        # base64 인코딩 실패 시 일반 video 사용
        st.warning(f"자동 재생을 위한 인코딩 실패: {e}")
        st.video(str(video_path))
    
    # 닫기 버튼
    if st.button("닫기", type="primary", width="stretch"):
        st.rerun()

