from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from moviepy import TextClip
from project_manager import project_manager


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
    
    @abstractmethod
    def render(self):
        """
        씬의 UI를 렌더링하는 메서드
        각 타입별로 구현해야 함
        """
        pass
    
    def generate_video_structure(self) -> Optional[str]:
        """
        비디오 파일을 생성하고 경로를 반환하는 메서드
        기본 구현: 1080x1920 크기의 가운데 정렬 텍스트 비디오 생성
        
        Returns:
            str: 생성된 비디오 파일 경로 또는 None (실패 시)
        """
        try:
            # 프로젝트 경로 가져오기
            project_path = project_manager.get_project_path()
            if not project_path:
                print("프로젝트가 로드되지 않았습니다.")
                return None
            
            # output 폴더 경로
            output_folder = project_path / "output"
            output_folder.mkdir(parents=True, exist_ok=True)
            
            # 비디오 파일 경로 (sceneid_output.mp4)
            output_filename = f"{self.scene_id}_output.mp4"
            output_path = output_folder / output_filename
            
            # 1080x1920 크기의 텍스트 클립 생성 (가운데 정렬)
            # MoviePy 2.x에서는 ColorClip을 사용하여 배경을 만들고 텍스트를 합성
            from moviepy import ColorClip, CompositeVideoClip
            
            # 배경 클립 생성 (1080x1920, 검은색)
            bg_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=3)
            
            # 텍스트 클립 생성 (가운데 정렬을 위해 horizontal_align, vertical_align 사용)
            txt_clip = TextClip(
                text="abc",
                font_size=100,
                color='white',
                duration=3,
                size=(1080, 1920),
                horizontal_align='center',
                vertical_align='center'
            )
            
            # 배경과 텍스트 합성
            final_clip = CompositeVideoClip([bg_clip, txt_clip], size=(1080, 1920))
            
            # 비디오 저장
            final_clip.write_videofile(str(output_path), fps=24)
            
            # 리소스 정리
            final_clip.close()
            txt_clip.close()
            bg_clip.close()
            
            # 상대 경로 반환 (output/sceneid_output.mp4)
            relative_path = f"output/{output_filename}"
            return relative_path
            
        except Exception as e:
            print(f"비디오 생성 중 오류 발생: {e}")
            return None
    
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

