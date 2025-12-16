import streamlit as st
from typing import Dict, Any


def render_type3(scene: Dict[str, Any]):
    """
    Type 3 씬의 UI를 렌더링하는 함수
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id, text, type 포함)
    """
    st.subheader(f"🎞️ Type 3 씬 - {scene.get('text', 'N/A')}")
    
    # Type 3 전용 UI 요소들
    st.write("**Type 3 전용 레이아웃**")
    
    # Type 3는 탭 레이아웃 사용
    tab1, tab2, tab3 = st.tabs(["기본 정보", "고급 설정", "미리보기"])
    
    with tab1:
        st.write("**씬 기본 정보**")
        st.json({
            "id": scene.get('id', 'N/A'),
            "type": scene.get('type', 'N/A'),
            "text": scene.get('text', 'N/A')
        })
    
    with tab2:
        st.write("**Type 3 고급 설정**")
        
        # Type 3 전용 라디오 버튼
        radio_option = st.radio(
            "Type 3 모드 선택",
            options=["모드 1", "모드 2", "모드 3"],
            key=f"type3_radio_{scene.get('id')}"
        )
        st.write(f"선택된 모드: {radio_option}")
        
        # Type 3 전용 멀티셀렉트
        multi_options = st.multiselect(
            "Type 3 추가 옵션",
            options=["옵션 X", "옵션 Y", "옵션 Z"],
            key=f"type3_multiselect_{scene.get('id')}"
        )
        if multi_options:
            st.write(f"선택된 옵션: {', '.join(multi_options)}")
    
    with tab3:
        st.write("**Type 3 미리보기**")
        st.info(f"씬 텍스트: {scene.get('text', 'N/A')}")
        st.info(f"씬 타입: {scene.get('type', 'N/A')}")
        st.info(f"씬 ID: {scene.get('id', 'N/A')[:8]}...")
    
    # Type 3 전용 파일 업로더 (예시)
    st.file_uploader(
        "Type 3 파일 업로드",
        key=f"type3_uploader_{scene.get('id')}",
        help="Type 3 씬에 파일을 업로드하세요"
    )
    
    st.divider()

