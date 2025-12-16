import streamlit as st
from typing import Dict, Any


def render_type1(scene: Dict[str, Any]):
    """
    Type 1 씬의 UI를 렌더링하는 함수
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id, text, type 포함)
    """
    st.subheader(f"🎬 Type 1 씬 - {scene.get('text', 'N/A')}")
    
    # Type 1 전용 UI 요소들
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**씬 정보**")
        st.write(f"- ID: {scene.get('id', 'N/A')[:8]}...")
        st.write(f"- Type: {scene.get('type', 'N/A')}")
        st.write(f"- Text: {scene.get('text', 'N/A')}")
    
    with col2:
        st.write("**Type 1 설정**")
        # Type 1 전용 설정 옵션들
        option1 = st.checkbox("옵션 1", key=f"type1_option1_{scene.get('id')}")
        option2 = st.checkbox("옵션 2", key=f"type1_option2_{scene.get('id')}")
        
        if option1:
            st.info("옵션 1이 활성화되었습니다.")
        if option2:
            st.info("옵션 2가 활성화되었습니다.")
    
    # Type 1 전용 입력 필드
    st.text_area(
        "Type 1 전용 텍스트 영역",
        value=scene.get('text', ''),
        key=f"type1_textarea_{scene.get('id')}",
        help="Type 1 씬의 텍스트를 입력하세요"
    )
    
    st.divider()

