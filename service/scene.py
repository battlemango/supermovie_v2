import uuid
from typing import Optional


class Scene:
    """씬 정보를 담는 클래스"""
    
    def __init__(self, scene_id: Optional[str] = None, text: str = "test", scene_type: str = "type1", **kwargs):
        """
        씬 정보 초기화
        
        Args:
            scene_id (str, optional): 씬의 고유 ID (없으면 자동 생성)
            text (str): 씬의 텍스트 내용 (기본값: "test")
            scene_type (str): 씬의 타입 (기본값: "type1")
            **kwargs: 추가적인 동적 속성들 (text 포함)
        """
        # ID가 없으면 UUID로 생성
        self.id = scene_id if scene_id else str(uuid.uuid4())
        self.type = scene_type  # type만 별도로 관리
        
        # 동적 속성 저장을 위한 딕셔너리 (id, type 제외, text 포함)
        self._data = {}
        # text를 _data에 저장
        self._data['text'] = text
        # kwargs로 전달된 추가 속성들을 _data에 저장
        for key, value in kwargs.items():
            if key not in ['id', 'type']:  # id와 type만 제외
                self._data[key] = value
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        딕셔너리에서 Scene 객체 생성 (팩토리 메서드)
        
        Args:
            data (dict): 씬 정보가 담긴 딕셔너리
            
        Returns:
            Scene: 생성된 Scene 객체
        """
        # id와 type만 별도로 추출
        scene_id = data.get("id")
        scene_type = data.get("type", "type1")
        
        # 나머지 모든 필드들(text 포함)을 kwargs로 전달
        kwargs = {k: v for k, v in data.items() if k not in ['id', 'type']}
        
        return cls(
            scene_id=scene_id,
            scene_type=scene_type,
            **kwargs
        )
    
    def to_dict(self) -> dict:
        """
        딕셔너리로 변환 (JSON 저장용)
        
        Returns:
            dict: 씬 정보 딕셔너리 (id, type + _data의 모든 필드 포함)
        """
        result = {
            "id": self.id,
            "type": self.type
        }
        # _data의 모든 필드들(text 포함)을 포함
        result.update(self._data)
        return result
    
    def __getitem__(self, key):
        """딕셔너리처럼 접근 가능하도록 구현 (기존 코드 호환성)"""
        if key == "id":
            return self.id
        elif key == "type":
            return self.type
        elif key in self._data:
            return self._data[key]
        else:
            raise KeyError(f"'{key}' 키가 존재하지 않습니다.")
    
    def __setitem__(self, key, value):
        """딕셔너리처럼 설정 가능하도록 구현"""
        if key == "id":
            self.id = value
        elif key == "type":
            self.type = value
        else:
            # text 포함 모든 동적 속성을 _data에 저장
            self._data[key] = value
    
    def __contains__(self, key):
        """'in' 연산자 지원"""
        return key == "id" or key == "type" or key in self._data
    
    @property
    def text(self):
        """text 속성 접근 (기존 코드 호환성)"""
        return self._data.get('text', 'test')
    
    @text.setter
    def text(self, value):
        """text 속성 설정 (기존 코드 호환성)"""
        self._data['text'] = value
    
    def get_field(self, key, default=None):
        """
        필드 값 가져오기
        
        Args:
            key (str): 필드 키
            default: 기본값 (키가 없을 때 반환)
            
        Returns:
            필드 값 또는 default
        """
        if key == "id":
            return self.id
        elif key == "type":
            return self.type
        else:
            # text 포함 모든 동적 필드는 _data에서 가져오기
            return self._data.get(key, default)
    
    def set_field(self, key, value):
        """
        필드 값 설정
        
        Args:
            key (str): 필드 키
            value: 설정할 값
        """
        if key == "id":
            self.id = value
        elif key == "type":
            self.type = value
        else:
            # text 포함 모든 동적 속성을 _data에 저장
            self._data[key] = value
    
    def __repr__(self):
        """씬 정보 문자열 표현"""
        return f"Scene(id='{self.id[:8]}...', text='{self.text}', type='{self.type}')"

