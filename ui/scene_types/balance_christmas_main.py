from pathlib import Path
import streamlit as st
from typing import Dict, Any
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

class BalanceChristmasMain(BaseSceneType):
    """Type 1 씬 타입 클래스"""
    def __init__(self, scene: Dict[str, Any]):
        super().__init__(scene)
    
    def render(self):
        """Type 1 씬의 UI를 렌더링"""
        # 텍스트 입력 컴포넌트 사용
        render_text_input(self.scene, "title", label="title", multiline=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            render_text_input(self.scene, "choice_a", label="A", multiline=False)
        with col2:
            render_text_input(self.scene, "choice_b", label="B", multiline=False)

        col1, col2 = st.columns([1, 1])
        with col1:
            render_image_input(self.scene, "a_image")
        with col2:
            render_image_input(self.scene, "b_image")
        
        col1, col2, col3 = st.columns([1, 1,1])
        with col1:
            render_audio_input(self.scene, "title_audio")
        with col2:
            render_audio_input(self.scene, "a_audio")
        with col3:
            render_audio_input(self.scene, "b_audio")      
             

    def generate_video_structure(self) -> str:
        title_audio_clip = self.gen_audio_clip("title_audio", 0)
        a_audio_clip = self.gen_audio_clip("a_audio", title_audio_clip.end)
        b_audio_clip = self.gen_audio_clip("b_audio", a_audio_clip.end)

        
        max_duration = round(b_audio_clip.end + 0.3, 1)
        print("max_duration : {max_duration}")
    
       
        base_clip = ColorClip(size=self.screen_size, color=(0, 0, 0), duration=max_duration)
        self.clips.append(base_clip)

        
        bg_clip = self.gen_image_clip(path="assets/balance/balance_bg.png",
                                       duration=max_duration, resized_width=1080, resized_height=1080, 
                                       position=("center", y_variabtion))
       
        self.gen_text_clip(text="크리스마스 밸런스",
                           font=FontUtils.MAPLESTORY_BOLD,
                           font_size=80,
                           start=0,
                           duration=max_duration,
                           position=("center", 200-960)
        )

       
        
        title_text_clip = self.gen_text_clip(field="title", color='black',font=FontUtils.MAPLESTORY_BOLD,start=0,duration=max_duration, size=(880, 1920),position=("center", 220-960+y_variabtion))
        a_text_clip = self.gen_text_clip(field="choice_a", font=FontUtils.MAPLESTORY_LIGHT,font_size=70,start=a_audio_clip.start,duration=max_duration,
                                         size=(480, 1920), position=(0, 800-960+y_variabtion), margin=(30,0))
        b_text_clip = self.gen_text_clip(field="choice_b", font=FontUtils.MAPLESTORY_LIGHT,font_size=70,start=b_audio_clip.start,duration=max_duration,
                                         size=(480, 1920), position=(540, 800-960+y_variabtion), margin=(30,0))
        
                    
        
        self.gen_image_clip(field="a_image", start=a_audio_clip.start, duration=max_duration, resized_width=300, position=(270-150, 400+y_variabtion))
        self.gen_image_clip(field="b_image", start=b_audio_clip.start, duration=max_duration,resized_width=300, position=(810-150, 400+y_variabtion))

        
        # 상대 경로 반환
        return self.generate_video(max_duration=max_duration)