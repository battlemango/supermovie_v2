import json
from pathlib import Path
from typing import List, Optional
from service.scene import Scene


class SceneManager:
    """씬을 포함한 JSON 파일을 관리하는 클래스"""
    
    def __init__(self, video_json_path: Optional[Path] = None):
        """
        SceneManager 초기화
        
        Args:
            video_json_path (Path, optional): video.json 파일 경로
        """
        self.video_json_path = video_json_path
        self.scenes: List[Scene] = []  # Scene 객체 리스트
        
        # 경로가 있으면 파일에서 로드
        if self.video_json_path:
            self.load()
    
    def set_path(self, video_json_path: Path):
        """
        video.json 파일 경로 설정 및 로드
        
        Args:
            video_json_path (Path): video.json 파일 경로
        """
        self.video_json_path = video_json_path
        self.load()
    
    def load(self):
        """video.json 파일에서 씬 데이터 로드"""
        if not self.video_json_path:
            self.scenes = []
            return
        
        # 파일이 있으면 읽기
        if self.video_json_path.exists():
            try:
                with open(self.video_json_path, 'r', encoding='utf-8') as f:
                    video_data = json.load(f)
                
                # scenes 배열을 Scene 객체 리스트로 변환
                scenes_data = video_data.get("scenes", [])
                self.scenes = [Scene.from_dict(scene_data) for scene_data in scenes_data]
            except Exception as e:
                print(f"video.json 읽기 오류: {e}")
                self.scenes = []
        else:
            # 파일이 없으면 빈 리스트로 초기화
            self.scenes = []
            # 빈 JSON 파일 생성
            self.save()
    
    def save(self) -> bool:
        """
        현재 씬 데이터를 video.json 파일에 저장
        
        Returns:
            bool: 저장 성공 여부
        """
        if not self.video_json_path:
            return False
        
        try:
            # Scene 객체들을 딕셔너리로 변환
            scenes_data = [scene.to_dict() for scene in self.scenes]
            video_data = {"scenes": scenes_data}
            
            # JSON 파일로 저장
            with open(self.video_json_path, 'w', encoding='utf-8') as f:
                json.dump(video_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"video.json 저장 오류: {e}")
            return False
    
    def add_scene(self, text: str = "test", scene_type: str = "type1") -> Optional[Scene]:
        """
        새로운 씬 추가
        
        Args:
            text (str): 씬의 텍스트 내용 (기본값: "test")
            scene_type (str): 씬의 타입 (기본값: "type1")
            
        Returns:
            Scene: 추가된 Scene 객체 또는 None (경로가 설정되지 않은 경우)
        """
        if not self.video_json_path:
            print("video.json 경로가 설정되지 않았습니다.")
            return None
        
        # 새로운 씬 생성
        new_scene = Scene(text=text, scene_type=scene_type)
        
        # 씬 리스트에 추가
        self.scenes.append(new_scene)
        
        # 변경사항 저장
        self.save()
        
        print(f"새 씬 추가됨: {new_scene}")
        return new_scene
    
    def get_scenes(self) -> List[Scene]:
        """
        현재 씬 리스트 반환
        
        Returns:
            List[Scene]: Scene 객체 리스트
        """
        return self.scenes
    
    def get_scene_by_id(self, scene_id: str) -> Optional[Scene]:
        """
        ID로 씬 찾기
        
        Args:
            scene_id (str): 찾을 씬의 ID
            
        Returns:
            Scene: 찾은 Scene 객체 또는 None
        """
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None
    
    def remove_scene(self, scene_id: str) -> bool:
        """
        ID로 씬 삭제
        
        Args:
            scene_id (str): 삭제할 씬의 ID
            
        Returns:
            bool: 삭제 성공 여부
        """
        scene = self.get_scene_by_id(scene_id)
        if scene:
            self.scenes.remove(scene)
            self.save()
            return True
        return False
    
    def update_scene_text(self, scene_id: str, text: str) -> bool:
        """
        씬의 텍스트 업데이트
        
        Args:
            scene_id (str): 업데이트할 씬의 ID
            text (str): 새로운 텍스트 내용
            
        Returns:
            bool: 업데이트 성공 여부
        """
        scene = self.get_scene_by_id(scene_id)
        if scene:
            scene.text = text
            self.save()
            return True
        return False
    
    def get_video_data(self) -> dict:
        """
        딕셔너리 형태로 비디오 데이터 반환 (기존 코드 호환성)
        
        Returns:
            dict: {"scenes": [...]} 형태의 딕셔너리
        """
        return {
            "scenes": [scene.to_dict() for scene in self.scenes]
        }

