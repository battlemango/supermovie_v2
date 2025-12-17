import streamlit as st
from typing import Dict, Any
from ui.components.text_component import render_text_input
from ui.components.image_component import render_image_input
from ui.scene_types.base_scene_type import BaseSceneType


class Type1Scene(BaseSceneType):
    """Type 1 씬 타입 클래스"""
    
    def render(self):
        """Type 1 씬의 UI를 렌더링"""
        # 텍스트 입력 컴포넌트 사용
        render_text_input(self.scene, "text", height=100, label="텍스트1")
        render_text_input(self.scene, "text2", height=100, label="텍스트2")
        
        # 이미지 입력 컴포넌트 사용
        render_image_input(self.scene, "image")
    
    def generate_video_structure(self) -> str:
        """
        Type 1 씬의 비디오 파일 생성
        기본 구현을 사용 (1080x1920, 가운데 텍스트)
        
        Returns:
            str: 생성된 비디오 파일 경로 또는 None
        """
        # 기본 구현 사용 (부모 클래스의 메서드 호출)
        return super().generate_video_structure()

