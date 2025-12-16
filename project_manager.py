import os
import datetime
from pathlib import Path
from service.video_manager import video_manager

class ProjectManager:
    """프로젝트 관리 클래스"""
    
    def __init__(self, base_dir="projects"):
        self.base_dir = Path(base_dir)
        self.current_project = None  # 현재 선택된 프로젝트 정보 저장
        self.ensure_projects_directory()

    def load_project(self, project):
        self.current_project = project
        video_manager.on_project_loaded(self.current_project)

    
    def ensure_projects_directory(self):
        """projects 디렉토리가 없으면 생성"""
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created projects directory: {self.base_dir}")
    
    def create_project(self, project_name):
        """
        프로젝트 생성 함수
        projects/날짜시간_이름 형태로 폴더 생성
        
        Args:
            project_name (str): 프로젝트 이름
            
        Returns:
            dict: 생성 결과 정보
        """
        try:
            # 현재 날짜시간 포맷 (YYYYMMDD_HHMMSS)
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            
            # 폴더 이름: 날짜시간_이름
            folder_name = f"{timestamp}_{project_name}"
            project_path = self.base_dir / folder_name
            
            # 프로젝트 폴더 생성
            project_path.mkdir(parents=True, exist_ok=True)
            
            # 기본 하위 폴더 생성
            subfolders = ['data', 'output', 'config', 'logs']
            for subfolder in subfolders:
                (project_path / subfolder).mkdir(exist_ok=True)
                        
            project_info = {
                "success": True,
                "project_name": project_name,
                "folder_name": folder_name,
                "project_path": str(project_path),
                "message": f"프로젝트 '{project_name}'가 성공적으로 생성되었습니다."
            }
            
            self.load_project(project_info)
            
            return project_info
            
        except Exception as e:
            return {
                "success": False,
                "project_name": project_name,
                "error": str(e),
                "message": f"프로젝트 생성 실패: {str(e)}"
            }
    
    def get_projects_list(self):
        """생성된 프로젝트 목록 반환"""
        if not self.base_dir.exists():
            return []
        
        projects = []
        for item in self.base_dir.iterdir():
            if item.is_dir():
                # 폴더 이름에서 날짜시간과 프로젝트 이름 분리
                folder_name = item.name
                if "_" in folder_name:
                    timestamp, name = folder_name.split("_", 1)
                    projects.append({
                        "folder_name": folder_name,
                        "project_name": name,
                        "timestamp": timestamp,
                        "path": str(item)
                    })
                else:
                    projects.append({
                        "folder_name": folder_name,
                        "project_name": folder_name,
                        "timestamp": "",
                        "path": str(item)
                    })
        
        return sorted(projects, key=lambda x: x["timestamp"], reverse=True)
    
    def get_current_project(self):
        """현재 선택된 프로젝트 정보 반환"""
        return self.current_project
    
    def delete_project(self, folder_name):
        """프로젝트 삭제"""
        try:
            project_path = self.base_dir / folder_name
            if project_path.exists():
                import shutil
                shutil.rmtree(project_path)
                return {
                    "success": True,
                    "message": f"프로젝트 '{folder_name}'가 삭제되었습니다."
                }
            else:
                return {
                    "success": False,
                    "message": f"프로젝트 '{folder_name}'를 찾을 수 없습니다."
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"삭제 실패: {str(e)}"
            }

# 전역 프로젝트 매니저 인스턴스
project_manager = ProjectManager()
