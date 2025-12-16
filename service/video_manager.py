import json
import os
import datetime
from pathlib import Path

class VideoManager:
    """프로젝트 관리 클래스"""
    
    def __init__(self, base_dir="projects"):
        self.base_dir = Path(base_dir)
        self.current_project = None
    
    def on_project_loaded(self, project):
        self.current_project = project

        print("on_project_loaded")
        
        if project and 'project_path' in project:
            project_path = Path(project['project_path'])
            video_json_path = project_path / 'video.json'

            
            print("on_project_loaded {project_path}")
            
            # video.json 파일이 있으면 읽기
            if video_json_path.exists():
                try:
                    with open(video_json_path, 'r', encoding='utf-8') as f:
                        self.video_data = json.load(f)
                except Exception as e:
                    print(f"video.json 읽기 오류: {e}")
                    self.video_data = {"scenes": []}
            else:
                # 없으면 빈 JSON 파일 생성
                self.video_data = {"scenes": []}
                try:
                    with open(video_json_path, 'w', encoding='utf-8') as f:
                        json.dump(self.video_data, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"video.json 생성 오류: {e}")
        else:
            self.video_data = {"scenes": []}
    
    def get_video_data(self):
        """현재 비디오 데이터 반환"""
        return self.video_data or {"scenes": []}
    
    def save_video_data(self):
        """현재 비디오 데이터 저장"""
        if self.current_project and 'project_path' in self.current_project:
            project_path = Path(self.current_project['project_path'])
            video_json_path = project_path / 'video.json'
            
            try:
                with open(video_json_path, 'w', encoding='utf-8') as f:
                    json.dump(self.video_data, f, ensure_ascii=False, indent=2)
                return True
            except Exception as e:
                print(f"video.json 저장 오류: {e}")
                return False
        return False    

# 전역 프로젝트 매니저 인스턴스
video_manager = VideoManager()
