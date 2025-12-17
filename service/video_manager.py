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
                
                
                # SceneManager에 경로 설정 및 로드
                self.scene_manager.set_path(video_json_path)
            else:
                # 경로가 없으면 SceneManager 초기화
                self.scene_manager = SceneManager()
        else:
            # 프로젝트가 없으면 SceneManager 초기화
            self.scene_manager = SceneManager()
    
    def get_video_data(self):
        return self.scene_manager.get_video_data()
    
    def add_scene(self, text="test", scene_type="type1"):
        if not self.current_project:
            print("프로젝트가 로드되지 않았습니다.")
            return None
        
        # SceneManager를 통해 씬 추가
        return self.scene_manager.add_scene(text=text, scene_type=scene_type)
    
    def update_scene_field(self, scene_id: str, key: str, value) -> bool:
        return self.scene_manager.update_scene_field(scene_id, key, value)
    
    def get_scene_field(self, scene_id: str, key: str, default=None):
        return self.scene_manager.get_scene_field(scene_id, key, default)
    
    def remove_scene(self, scene_id: str) -> bool:
        return self.scene_manager.remove_scene(scene_id)
    
    def save_video_data(self):
        return self.scene_manager.save()    

# 전역 프로젝트 매니저 인스턴스
video_manager = VideoManager()
