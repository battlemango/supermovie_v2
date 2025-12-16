import streamlit as st
from typing import Dict, Any


def render_type2(scene: Dict[str, Any]):
    """
    Type 2 씬의 UI를 렌더링하는 함수
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id, text, type 포함)
    """
    st.subheader(f"🎥 Type 2 씬 - {scene.get('text', 'N/A')}")
    
    # Type 2 전용 UI 요소들
    st.write("**Type 2 전용 레이아웃**")
    
    # Type 2는 3열 레이아웃 사용
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("씬 ID", scene.get('id', 'N/A')[:8] + "...")
    
    with col2:
        st.metric("타입", scene.get('type', 'N/A'))
    
    with col3:
        # Type 2 전용 슬라이더
        value = st.slider(
            "Type 2 설정값",
            min_value=0,
            max_value=100,
            value=50,
            key=f"type2_slider_{scene.get('id')}"
        )
        st.write(f"현재 값: {value}")
    
    # Type 2 전용 선택 박스
    st.selectbox(
        "Type 2 옵션 선택",
        options=["옵션 A", "옵션 B", "옵션 C"],
        key=f"type2_select_{scene.get('id')}",
        help="Type 2 씬의 옵션을 선택하세요"
    )
    
    # Type 2 전용 텍스트 입력
    st.text_input(
        "Type 2 전용 입력",
        value=scene.get('text', ''),
        key=f"type2_input_{scene.get('id')}",
        help="Type 2 씬의 텍스트를 입력하세요"
    )
    
    st.divider()

