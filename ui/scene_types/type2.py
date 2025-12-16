import streamlit as st
from typing import Dict, Any
from ui.scene_types.base_scene_type import BaseSceneType


class Type2Scene(BaseSceneType):
    """Type 2 씬 타입 클래스"""
    
    def render(self):
        """Type 2 씬의 UI를 렌더링"""
        st.subheader(f"🎥 Type 2 씬 - {self.get_field('text', 'N/A')}")
        
        # Type 2 전용 UI 요소들
        st.write("**Type 2 전용 레이아웃**")
        
        # Type 2는 3열 레이아웃 사용
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("씬 ID", self.scene_id[:8] + "..." if self.scene_id else 'N/A')
        
        with col2:
            st.metric("타입", self.scene_type)
        
        with col3:
            # Type 2 전용 슬라이더
            value = st.slider(
                "Type 2 설정값",
                min_value=0,
                max_value=100,
                value=50,
                key=f"type2_slider_{self.scene_id}"
            )
            st.write(f"현재 값: {value}")
        
        # Type 2 전용 선택 박스
        st.selectbox(
            "Type 2 옵션 선택",
            options=["옵션 A", "옵션 B", "옵션 C"],
            key=f"type2_select_{self.scene_id}",
            help="Type 2 씬의 옵션을 선택하세요"
        )
        
        # Type 2 전용 텍스트 입력
        st.text_input(
            "Type 2 전용 입력",
            value=self.get_field('text', ''),
            key=f"type2_input_{self.scene_id}",
            help="Type 2 씬의 텍스트를 입력하세요"
        )
        
        st.divider()
    
    def generate_video_structure(self) -> Dict[str, Any]:
        """
        Type 2 씬의 비디오 생성 구조 반환
        Type 2는 슬라이더와 옵션을 사용한 비디오 구조를 생성
        
        Returns:
            dict: 비디오 생성에 필요한 구조 데이터
        """
        return {
            "type": "type2",
            "text": self.get_field("text", ""),
            "scene_id": self.scene_id
            # Type 2 전용 필드들을 여기에 추가
        }

