import uuid
from typing import Optional


class Scene:
    """씬 정보를 담는 클래스"""
    
    def __init__(self, scene_id: Optional[str] = None, text: str = "test", scene_type: str = "type1"):
        """
        씬 정보 초기화
        
        Args:
            scene_id (str, optional): 씬의 고유 ID (없으면 자동 생성)
            text (str): 씬의 텍스트 내용 (기본값: "test")
            scene_type (str): 씬의 타입 (기본값: "type1")
        """
        # ID가 없으면 UUID로 생성
        self.id = scene_id if scene_id else str(uuid.uuid4())
        self.text = text
        self.type = scene_type
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        딕셔너리에서 Scene 객체 생성 (팩토리 메서드)
        
        Args:
            data (dict): 씬 정보가 담긴 딕셔너리
            
        Returns:
            Scene: 생성된 Scene 객체
        """
        return cls(
            scene_id=data.get("id"),
            text=data.get("text", "test"),
            scene_type=data.get("type", "type1")  # 기본값 type1
        )
    
    def to_dict(self) -> dict:
        """
        딕셔너리로 변환 (JSON 저장용)
        
        Returns:
            dict: 씬 정보 딕셔너리
        """
        return {
            "id": self.id,
            "text": self.text,
            "type": self.type
        }
    
    def __getitem__(self, key):
        """딕셔너리처럼 접근 가능하도록 구현 (기존 코드 호환성)"""
        if key == "id":
            return self.id
        elif key == "text":
            return self.text
        elif key == "type":
            return self.type
        else:
            raise KeyError(f"'{key}' 키가 존재하지 않습니다.")
    
    def __contains__(self, key):
        """'in' 연산자 지원"""
        return key in ["id", "text", "type"]
    
    def __repr__(self):
        """씬 정보 문자열 표현"""
        return f"Scene(id='{self.id[:8]}...', text='{self.text}', type='{self.type}')"

