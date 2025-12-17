import streamlit as st
from typing import Dict, Any
from ui.components.text_component import render_text_input
from ui.components.image_component import render_image_input
from ui.components.audio_component import render_audio_input
from ui.scene_types.base_scene_type import BaseSceneType
from moviepy import CompositeAudioClip, TextClip, AudioFileClip
from project_manager import project_manager


class BalanceChristmasMain(BaseSceneType):
    """Type 1 씬 타입 클래스"""
    
    def render(self):
        """Type 1 씬의 UI를 렌더링"""
        # 텍스트 입력 컴포넌트 사용
        render_text_input(self.scene, "title", label="title")
        
        # choice_a와 a_image를 한 컬럼에, choice_b와 b_image를 다른 컬럼에 배치
        col1, col2 = st.columns(2)
        
        with col1:
            # A 선택지와 A 이미지를 같은 컬럼에 배치
            render_text_input(self.scene, "choice_a", label="A")
            render_image_input(self.scene, "a_image")
            render_audio_input(self.scene, "a_audio")
        
        with col2:
            # B 선택지와 B 이미지를 같은 컬럼에 배치
            render_text_input(self.scene, "choice_b", label="B")
            render_image_input(self.scene, "b_image")
            render_audio_input(self.scene, "b_audio")

    
    def generate_video_structure(self) -> str:
        title = self.scene.get("title", "")
        choice_a = self.scene.get("choice_a", "")
        choice_b = self.scene.get("choice_b", "")

        a_image = self.scene.get("a_image", "")
        b_image = self.scene.get("b_image", "")

        
        a_audio = self.scene.get("a_audio", "")
        b_audio = self.scene.get("b_audio", "")

        print(f"{title}, {choice_a}, {choice_b}, {a_image}, {b_image}, {a_audio}, {b_audio}")

        try:
            # project_manager를 통해 output 경로 가져오기
            output_folder, output_path, relative_path = project_manager.get_output_path(self.scene_id)
            if not output_path:
                return None
            
            # MoviePy 임포트
            from moviepy import ColorClip, CompositeVideoClip, ImageClip
            
            # 배경 클립 생성 (1080x1920, 검은색, 5초)
            max_duration = 5
            bg_clip = ColorClip(size=self.screen_size, color=(0, 0, 0), duration=max_duration)
            
            clips = []
            clips.append(bg_clip)
            audio_clips = []
            
            
            if a_audio:
                full_audio_path = project_manager.get_audio_path(a_audio)
                if full_audio_path and full_audio_path.exists():
                    a_audio_clip = AudioFileClip(full_audio_path).with_start(0)
                    audio_clips.append(a_audio_clip)
            
            if b_audio:
                full_audio_path = project_manager.get_audio_path(b_audio)
                if full_audio_path and full_audio_path.exists():
                    b_audio_clip = AudioFileClip(full_audio_path).with_start(a_audio_clip.end)
                    audio_clips.append(b_audio_clip)

            # 1초: title 텍스트
            if title:
                title_clip = TextClip(
                    text=title,
                    font_size=80,
                    color='white',
                    method='caption',
                    size=self.screen_size,
                )
                title_clip = title_clip.with_start(0).with_duration(max_duration).with_position(("center", 300))
                clips.append(title_clip)
            
            # 2초: choice_a 텍스트
            if choice_a:
                choice_a_clip = TextClip(
                    text=choice_a,
                    font_size=80,
                    color='white',
                    method='caption',
                    size=(540, 1920),
                )
                
                choice_a_clip = choice_a_clip.with_start(1).with_duration(max_duration).with_position((0, 200))
                clips.append(choice_a_clip)
            
            # 3초: choice_b 텍스트
            if choice_b:
                choice_b_clip = TextClip(
                    text=choice_b,
                    font_size=80,
                    method='caption',
                    size=(540, 1920),
                    color='white',
                )
                choice_b_clip = choice_b_clip.with_start(2).with_duration(max_duration).with_position((540, 100))
                clips.append(choice_b_clip)
            
            # 4초: a_image 이미지
            if a_image:
                # 프로젝트 경로 기준으로 전체 이미지 경로 가져오기
                full_image_path = project_manager.get_image_path(a_image)
                if full_image_path and full_image_path.exists():
                    a_img_clip = ImageClip(str(full_image_path), duration=1)
                    a_img_clip = a_img_clip.with_start(1).with_duration(max_duration).with_position((300, 800))
                    clips.append(a_img_clip)
            
            # 5초: b_image 이미지
            if b_image:
                # 프로젝트 경로 기준으로 전체 이미지 경로 가져오기
                full_image_path = project_manager.get_image_path(b_image)
                if full_image_path and full_image_path.exists():
                    b_img_clip = ImageClip(str(full_image_path), duration=1)
                    b_img_clip = b_img_clip.with_start(2).with_duration(max_duration).with_position((700, 800))
                    clips.append(b_img_clip)

                
            
            # 모든 클립을 연결하여 최종 비디오 생성
            if clips:
                final_audio = CompositeAudioClip(audio_clips)
                final_clip = CompositeVideoClip(clips).with_audio(final_audio)
            else:
                # 컨텐츠가 없는 경우 빈 비디오 생성
                final_clip = bg_clip
            
            final_clip = final_clip.with_duration(max_duration)
            # 비디오 저장
            final_clip.write_videofile(str(output_path), fps=self.fps)
            
            # 리소스 정리
            final_clip.close()
            bg_clip.close()
            for clip in clips:
                clip.close()
            
            # 상대 경로 반환
            return relative_path
            
        except Exception as e:
            print(f"비디오 생성 중 오류 발생: {e}")
            return None
