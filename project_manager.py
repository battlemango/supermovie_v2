import os
import datetime
from pathlib import Path
from service.video_manager import video_manager


class Project:
    """프로젝트 정보를 담는 클래스 - 일관된 인터페이스 제공"""
    
    def __init__(self, project_name, folder_name, path, timestamp=None):
        """
        프로젝트 정보 초기화
        
        Args:
            project_name (str): 프로젝트 이름
            folder_name (str): 폴더 이름 (타임스탬프 포함)
            path (str or Path): 프로젝트 경로
            timestamp (str, optional): 타임스탬프
        """
        self.project_name = project_name
        self.folder_name = folder_name
        # path를 Path 객체로 변환하여 저장 (일관성 유지)
        self.path = Path(path) if not isinstance(path, Path) else path
        self.timestamp = timestamp or ""
    
    def __getitem__(self, key):
        """딕셔너리처럼 접근 가능하도록 구현 (기존 코드 호환성)"""
        # project_path와 path 모두 지원 (하위 호환성)
        if key == "project_path":
            return str(self.path)
        elif key == "path":
            return str(self.path)
        elif hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' 키가 존재하지 않습니다.")
    
    def __contains__(self, key):
        """'in' 연산자 지원"""
        return key in ["project_name", "folder_name", "path", "project_path", "timestamp"]
    
    def to_dict(self):
        """딕셔너리로 변환 (기존 코드 호환성)"""
        return {
            "project_name": self.project_name,
            "folder_name": self.folder_name,
            "path": str(self.path),
            "project_path": str(self.path),  # 하위 호환성을 위해 둘 다 포함
            "timestamp": self.timestamp
        }
    
    def __repr__(self):
        """프로젝트 정보 문자열 표현"""
        return f"Project(name='{self.project_name}', path='{self.path}')"


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
            
            # Project 객체 생성
            project = Project(
                project_name=project_name,
                folder_name=folder_name,
                path=project_path,
                timestamp=timestamp
            )
            
            self.load_project(project)
            
            # 반환값은 딕셔너리 형태로 (기존 코드 호환성)
            return {
                "success": True,
                "project_name": project_name,
                "folder_name": folder_name,
                "project_path": str(project_path),
                "path": str(project_path),  # 일관성을 위해 path도 포함
                "timestamp": timestamp,
                "message": f"프로젝트 '{project_name}'가 성공적으로 생성되었습니다."
            }
            
        except Exception as e:
            return {
                "success": False,
                "project_name": project_name,
                "error": str(e),
                "message": f"프로젝트 생성 실패: {str(e)}"
            }
    
    def get_projects_list(self):
        """생성된 프로젝트 목록 반환 (Project 객체 리스트)"""
        if not self.base_dir.exists():
            return []
        
        projects = []
        for item in self.base_dir.iterdir():
            if item.is_dir():
                # 폴더 이름에서 날짜시간과 프로젝트 이름 분리
                folder_name = item.name
                if "_" in folder_name:
                    timestamp, name = folder_name.split("_", 1)
                    # Project 객체 생성
                    project = Project(
                        project_name=name,
                        folder_name=folder_name,
                        path=item,
                        timestamp=timestamp
                    )
                    projects.append(project)
                else:
                    # 타임스탬프가 없는 경우
                    project = Project(
                        project_name=folder_name,
                        folder_name=folder_name,
                        path=item,
                        timestamp=""
                    )
                    projects.append(project)
        
        # 타임스탬프 기준으로 정렬 (최신순)
        return sorted(projects, key=lambda x: x.timestamp, reverse=True)
    
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
