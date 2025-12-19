from pathlib import Path
import streamlit as st
from typing import Dict, Any
from service.tts_service import TTSRequest
from ui.components.text_component import render_text_input
from ui.components.image_component import render_image_input
from ui.components.audio_component import render_audio_input
from ui.scene_types.base_scene_type import BaseSceneType
from moviepy import CompositeAudioClip, TextClip, AudioFileClip
from project_manager import project_manager
from utils import FontUtils

# MoviePy 임포트
from moviepy import ColorClip, CompositeVideoClip, ImageClip

y_variabtion = 300

class BalanceChristmasEnter(BaseSceneType):
    """Type 1 씬 타입 클래스"""
    def __init__(self, scene: Dict[str, Any]):
        super().__init__(scene)
    
    def render(self):
        """Type 1 씬의 UI를 렌더링"""
        # 텍스트 입력 컴포넌트 사용
        render_text_input(self.scene, "title", label="title")

        # 이미지 입력 컴포넌트 사용
        render_image_input(self.scene, "center_image")
        title_text = self.scene.get("title")
        tts_request = None
        if title_text:
            tts_request = TTSRequest.han(text=title_text)
        render_audio_input(self.scene, "title_audio", tts_request)

    def generate_video_structure(self) -> str:
        title_audio_clip = self.gen_audio_clip("title_audio", 0)        
        max_duration = round(title_audio_clip.end)
        print("max_duration : {max_duration}")
       
        base_clip = ColorClip(size=self.screen_size, color=(255, 255, 255), duration=max_duration)
        self.clips.append(base_clip)

        
        # bg_clip = self.gen_image_clip(path="assets/balance/christmas_bal_title_bg.png",
        #                                duration=max_duration, resized_width=1080, resized_height=1080, 
        #                                position=("center", y_variabtion))
       
    
        title_text_clip = self.gen_text_clip(field="title", font=FontUtils.MAPLESTORY_BOLD,color='black',start=0,duration=max_duration, position=("center", 200-960+y_variabtion))
                    
        
        self.gen_image_clip(field="center_image", start=0.5, duration=max_duration, resized_width=300, position=("center", 400+y_variabtion))
        
        
        # 상대 경로 반환
        return self.generate_video(max_duration=max_duration)