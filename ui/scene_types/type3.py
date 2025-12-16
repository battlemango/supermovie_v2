import streamlit as st
from typing import Dict, Any
from ui.scene_types.base_scene_type import BaseSceneType


class Type3Scene(BaseSceneType):
    """Type 3 씬 타입 클래스"""
    
    def render(self):
        """Type 3 씬의 UI를 렌더링"""
        st.subheader(f"🎞️ Type 3 씬 - {self.get_field('text', 'N/A')}")
        
        # Type 3 전용 UI 요소들
        st.write("**Type 3 전용 레이아웃**")
        
        # Type 3는 탭 레이아웃 사용
        tab1, tab2, tab3 = st.tabs(["기본 정보", "고급 설정", "미리보기"])
        
        with tab1:
            st.write("**씬 기본 정보**")
            st.json({
                "id": self.scene_id,
                "type": self.scene_type,
                "text": self.get_field('text', 'N/A')
            })
        
        with tab2:
            st.write("**Type 3 고급 설정**")
            
            # Type 3 전용 라디오 버튼
            radio_option = st.radio(
                "Type 3 모드 선택",
                options=["모드 1", "모드 2", "모드 3"],
                key=f"type3_radio_{self.scene_id}"
            )
            st.write(f"선택된 모드: {radio_option}")
            
            # Type 3 전용 멀티셀렉트
            multi_options = st.multiselect(
                "Type 3 추가 옵션",
                options=["옵션 X", "옵션 Y", "옵션 Z"],
                key=f"type3_multiselect_{self.scene_id}"
            )
            if multi_options:
                st.write(f"선택된 옵션: {', '.join(multi_options)}")
        
        with tab3:
            st.write("**Type 3 미리보기**")
            st.info(f"씬 텍스트: {self.get_field('text', 'N/A')}")
            st.info(f"씬 타입: {self.scene_type}")
            st.info(f"씬 ID: {self.scene_id[:8]}..." if self.scene_id else "N/A")
        
        # Type 3 전용 파일 업로더 (예시)
        st.file_uploader(
            "Type 3 파일 업로드",
            key=f"type3_uploader_{self.scene_id}",
            help="Type 3 씬에 파일을 업로드하세요"
        )
        
        st.divider()
    
    def generate_video_structure(self) -> Dict[str, Any]:
        """
        Type 3 씬의 비디오 생성 구조 반환
        Type 3는 탭과 고급 설정을 사용한 비디오 구조를 생성
        
        Returns:
            dict: 비디오 생성에 필요한 구조 데이터
        """
        return {
            "type": "type3",
            "text": self.get_field("text", ""),
            "scene_id": self.scene_id
            # Type 3 전용 필드들을 여기에 추가
        }

