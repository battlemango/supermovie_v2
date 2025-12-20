from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from moviepy import AudioFileClip, CompositeAudioClip, CompositeVideoClip, ImageClip, TextClip
from project_manager import project_manager
from utils import FontUtils
from service.text_image_service import text_image_service
import tempfile


class BaseSceneType(ABC):
    """씬 타입의 기본 클래스 - 모든 씬 타입이 상속받아야 함"""
    
    def __init__(self, scene: Dict[str, Any]):
        """
        씬 타입 초기화
        
        Args:
            scene (dict): 씬 정보 딕셔너리 (id, text, type 포함)
        """
        self.scene = scene
        self.scene_id = scene.get('id')
        self.scene_type = scene.get('type', 'type1')
        self.fps = project_manager.get_fps()
        self.screen_size = project_manager.get_screen_size()

        self.clips = []
        self.audio_clips = []
    
    @abstractmethod
    def render(self):
        """
        씬의 UI를 렌더링하는 메서드
        각 타입별로 구현해야 함
        """
        pass
    
    @abstractmethod
    def generate_video_structure(self) -> Optional[str]:
        pass
    
    def get_field(self, field: str, default=None):
        """
        씬의 필드 값 가져오기 (편의 메서드)
        
        Args:
            field (str): 필드명
            default: 기본값
            
        Returns:
            필드 값 또는 default
        """
        return self.scene.get(field, default)


    def generate_video(self, max_duration) -> str:
        try:
            # project_manager를 통해 output 경로 가져오기
            output_folder, output_path, relative_path = project_manager.get_output_path(self.scene_id)
            if not output_path:
                return None            
            # 모든 클립을 연결하여 최종 비디오 생성
            if self.clips:
                final_audio = CompositeAudioClip(self.audio_clips)
                final_clip = CompositeVideoClip(self.clips).with_audio(final_audio)
            
            final_clip = final_clip.with_duration(max_duration)
            # 비디오 저장
            final_clip.write_videofile(str(output_path), fps=self.fps)
            
            # 리소스 정리
            final_clip.close()
            for clip in self.clips:
                clip.close()
            
            # 상대 경로 반환
            return relative_path
            
        except Exception as e:
            print(f"비디오 생성 중 오류 발생: {e}")
            return None

    def gen_audio_clip(self, field, start=0):
        audio_path = self.scene.get(field, None)
        if not audio_path:
            return None
        
        full_audio_path = project_manager.get_relative_path(audio_path)
        if full_audio_path and full_audio_path.exists():
            audio_clip = AudioFileClip(full_audio_path).with_start(start)
            self.audio_clips.append(audio_clip)
            return audio_clip

        return None
    
    def gen_image_clip(self, field=None, path=None, start=0, end= -1, duration= 1, resized_width = -1, resized_height=-1, position=("center", "center")):
        if not path:
            image_path = self.scene.get(field, None)
            if not image_path:
                return None
            else:
                full_path = project_manager.get_relative_path(image_path)
        else:
            full_path = path
        
        
        if full_path:
            
            if end != -1:
                clip = ImageClip(str(full_path)).with_start(start).with_position(position).with_end(end)
            else:
                clip = ImageClip(str(full_path), duration=duration).with_start(start).with_position(position)
            
            if resized_width != -1 and resized_height != -1:
                clip = clip.resized(width=resized_width, height=resized_height)
            elif resized_width != -1:
                clip = clip.resized(width=resized_width)
            elif resized_height != -1:
                clip = clip.resized(height=resized_height)

            self.clips.append(clip)
                
            return clip

        return None
    
    def gen_text_clip(self, text=None, field=None, font=FontUtils.MAPLESTORY_LIGHT,font_size=80,color='white',method='caption',margin=(0,0),size=(1080,1920),start=0, end= -1, duration= 1, position=("center", "center")):
        if not text:
            text = self.scene.get(field, None)
        if not text:
            return None
        
        clip = TextClip(
                font=font,
                text=text,
                font_size=font_size,
                color=color,
                method=method,
                margin=margin,
                size=size,
                text_align="center"
            )
        if end != -1:
            clip = clip.with_start(start).with_end(end).with_position(position)
        else:
            clip = clip.with_start(start).with_duration(duration).with_position(position)

        self.clips.append(clip)
        return clip
    
    def gen_rich_text_clip(
        self,
        text=None,
        field=None,
        font=FontUtils.MAPLESTORY_LIGHT,
        font_size=80,
        color='white',
        screen_size=(1080, 1920),
        text_width=1080,
        margin=(0, 0),
        text_align="center",
        start=0,
        end=-1,
        duration=1,
        position=(540, 960)
    ):
        """
        텍스트를 이미지로 변환하여 ImageClip으로 생성하는 메서드
        
        Args:
            text (str, optional): 텍스트 (없으면 field에서 가져옴)
            field (str, optional): 씬 필드명
            font (str): 폰트 경로
            font_size (int): 폰트 크기
            color (str): 텍스트 색상
            screen_size (tuple): 캔버스 크기 (width, height) - 전체 이미지 크기
            text_width (int): 텍스트 한 줄 너비
            margin (tuple): 여백 (x, y) - 현재 미사용
            text_align (str): 텍스트 정렬 ("center", "left", "right")
            start (float): 시작 시간
            end (float): 종료 시간 (-1이면 duration 사용)
            duration (float): 지속 시간
            position (tuple): 캔버스 내에서 텍스트를 그릴 중점 위치 (x, y)
                             텍스트는 position - (text_width/2, text_height/2)부터 그려짐
                             ImageClip은 center로 배치됨
        
        Returns:
            ImageClip: 생성된 이미지 클립 또는 None
        """
        # 텍스트 가져오기
        if not text:
            text = self.scene.get(field, None) if field else None
        
        if not text:
            return None
        
        try:
            # TextImage 서비스를 사용하여 텍스트를 이미지로 변환
            # screen_size는 캔버스 크기, position은 텍스트를 그릴 중점 위치
            text_image = text_image_service.create_text_image(
                text=text,
                font_path=font,
                font_size=font_size,
                color=color,
                screen_size=screen_size,
                text_width=text_width,
                position=position,
                text_align=text_align
            )
            
            if not text_image:
                return None
            
            # 프로젝트 폴더의 temp 폴더에 저장 (상태 확인용)
            project_path = project_manager.get_project_path()
            if project_path:
                # temp 폴더 생성
                temp_folder = project_path / "temp"
                temp_folder.mkdir(parents=True, exist_ok=True)
                
                # 파일명 생성 (scene_id와 텍스트 해시 사용)
                import hashlib
                text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                filename = f"{self.scene_id}_text_{text_hash}.png"
                tmp_path = temp_folder / filename
            else:
                # 프로젝트가 없으면 시스템 임시 디렉토리 사용
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    tmp_path = Path(tmp_file.name)
            
            # 이미지 저장
            text_image.save(tmp_path, 'PNG')
            print(f"[TEXT_IMAGE] 텍스트 이미지 저장: {tmp_path}")
            
            # ImageClip 생성 (position은 이미 텍스트 그릴 때 적용했으므로 center로 설정)
            if end != -1:
                clip = ImageClip(str(tmp_path)).with_start(start).with_position("center").with_end(end)
            else:
                clip = ImageClip(str(tmp_path), duration=duration).with_start(start).with_position("center")
            
            # clips에 추가
            self.clips.append(clip)
            
            return clip
            
        except Exception as e:
            print(f"rich text clip 생성 중 오류 발생: {e}")
            return None
    
    
