from abc import ABC, abstractmethod
from typing import Dict, Any


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
    
    @abstractmethod
    def generate_video_structure(self) -> Dict[str, Any]:
        """
        비디오 생성을 위한 구조를 생성하는 메서드
        각 타입별로 다른 방식으로 구현
        
        Returns:
            dict: 비디오 생성에 필요한 구조 데이터
        """
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

