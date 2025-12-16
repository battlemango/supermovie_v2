import json
import os
import datetime
from pathlib import Path
from service.scene_manager import SceneManager

class VideoManager:
    """비디오 프로젝트 관리 클래스"""
    
    def __init__(self, base_dir="projects"):
        self.base_dir = Path(base_dir)
        self.current_project = None
        # SceneManager를 멤버변수로 선언
        self.scene_manager = SceneManager()
    
    def on_project_loaded(self, project):
        """프로젝트가 로드되었을 때 호출되는 메서드"""
        self.current_project = project

        print("on_project_loaded")
        
        # Project 객체 또는 딕셔너리 모두 지원
        if project:
            # Project 객체인 경우 path 속성 사용, 딕셔너리인 경우 project_path 또는 path 키 사용
            if hasattr(project, 'path'):
                # Project 객체인 경우
                project_path = project.path
            elif 'project_path' in project:
                # 딕셔너리이고 project_path 키가 있는 경우
                project_path = Path(project['project_path'])
            elif 'path' in project:
                # 딕셔너리이고 path 키가 있는 경우
                project_path = Path(project['path'])
            else:
                project_path = None
            
            if project_path:
                video_json_path = project_path / 'video.json'
                
                print(f"on_project_loaded: {project_path}")
                
                # SceneManager에 경로 설정 및 로드
                self.scene_manager.set_path(video_json_path)
            else:
                # 경로가 없으면 SceneManager 초기화
                self.scene_manager = SceneManager()
        else:
            # 프로젝트가 없으면 SceneManager 초기화
            self.scene_manager = SceneManager()
    
    def get_video_data(self):
        """
        현재 비디오 데이터 반환 (딕셔너리 형태, 기존 코드 호환성)
        
        Returns:
            dict: {"scenes": [...]} 형태의 딕셔너리
        """
        return self.scene_manager.get_video_data()
    
    def add_scene(self, text="test", scene_type="type1"):
        """
        새로운 씬을 추가하는 함수
        
        Args:
            text (str): 씬의 텍스트 내용 (기본값: "test")
            scene_type (str): 씬의 타입 (기본값: "type1")
            
        Returns:
            Scene: 추가된 Scene 객체 또는 None (프로젝트가 로드되지 않은 경우)
        """
        # 프로젝트가 로드되지 않은 경우
        if not self.current_project:
            print("프로젝트가 로드되지 않았습니다.")
            return None
        
        # SceneManager를 통해 씬 추가
        return self.scene_manager.add_scene(text=text, scene_type=scene_type)
    
    def update_scene_text(self, scene_id: str, text: str) -> bool:
        """
        씬의 텍스트 업데이트
        
        Args:
            scene_id (str): 업데이트할 씬의 ID
            text (str): 새로운 텍스트 내용
            
        Returns:
            bool: 업데이트 성공 여부
        """
        return self.scene_manager.update_scene_text(scene_id, text)
    
    def update_scene_field(self, scene_id: str, key: str, value) -> bool:
        """
        씬의 특정 필드 업데이트 (동적 필드 지원)
        type마다 자유롭게 필드를 추가하고 수정할 수 있습니다.
        
        Args:
            scene_id (str): 업데이트할 씬의 ID
            key (str): 필드 키 (예: "title", "duration", "settings" 등)
            value: 설정할 값 (문자열, 숫자, 딕셔너리, 리스트 등 모든 타입 가능)
            
        Returns:
            bool: 업데이트 성공 여부
            
        Example:
            video_manager.update_scene_field("scene-id", "title", "새로운 제목")
            video_manager.update_scene_field("scene-id", "duration", 30)
            video_manager.update_scene_field("scene-id", "settings", {"volume": 0.8})
        """
        return self.scene_manager.update_scene_field(scene_id, key, value)
    
    def get_scene_field(self, scene_id: str, key: str, default=None):
        """
        씬의 특정 필드 값 가져오기 (동적 필드 지원)
        type마다 자유롭게 저장한 필드를 가져올 수 있습니다.
        
        Args:
            scene_id (str): 씬의 ID
            key (str): 필드 키
            default: 기본값 (키가 없을 때 반환)
            
        Returns:
            필드 값 또는 default
            
        Example:
            title = video_manager.get_scene_field("scene-id", "title", "기본 제목")
            duration = video_manager.get_scene_field("scene-id", "duration", 0)
            settings = video_manager.get_scene_field("scene-id", "settings", {})
        """
        return self.scene_manager.get_scene_field(scene_id, key, default)
    
    def save_video_data(self):
        """
        현재 비디오 데이터 저장 (SceneManager를 통해 저장)
        
        Returns:
            bool: 저장 성공 여부
        """
        return self.scene_manager.save()    

# 전역 프로젝트 매니저 인스턴스
video_manager = VideoManager()
