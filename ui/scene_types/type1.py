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
    
    def generate_video_structure(self) -> Dict[str, Any]:
        """
        Type 1 씬의 비디오 생성 구조 반환
        Type 1은 텍스트와 이미지를 사용한 비디오 구조를 생성
        
        Returns:
            dict: 비디오 생성에 필요한 구조 데이터
        """
        return {
            "type": "type1",
            "text": self.get_field("text", ""),
            "text2": self.get_field("text2", ""),
            "image": self.get_field("image", None),
            "scene_id": self.scene_id
        }

