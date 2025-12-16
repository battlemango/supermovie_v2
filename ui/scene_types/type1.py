import streamlit as st
from typing import Dict, Any
from ui.components.text_component import render_text_input
from ui.components.image_component import render_image_input


def render_type1(scene: Dict[str, Any]):
    """
    Type 1 씬의 UI를 렌더링하는 함수
    텍스트 영역과 이미지 업로드 기능을 제공합니다.
    
    Args:
        scene (dict): 씬 정보 딕셔너리 (id, text, type 포함)
    """
    # 텍스트 입력 컴포넌트 사용
    render_text_input(scene, "text", height=100, label="텍스트1")
    render_text_input(scene, "text2", height=100, label="텍스트2")
    
    # 이미지 입력 컴포넌트 사용
    render_image_input(scene, "image")

