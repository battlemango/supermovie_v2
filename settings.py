import json
import os
from pathlib import Path


class Settings:
    """설정을 관리하는 정적 클래스"""
    
    _settings_file = "settings.json"
    _settings = {}
    
    @classmethod
    def load_settings(cls):
        """설정 파일에서 설정을 로드합니다."""
        try:
            settings_path = Path(cls._settings_file)
            if settings_path.exists():
                with open(settings_path, 'r', encoding='utf-8') as f:
                    cls._settings = json.load(f)
            else:
                # 파일이 없으면 기본 설정으로 생성
                cls._settings = {
                    "last_project": None,
                    "debug_mode": False
                }
                cls.save_settings()
        except Exception as e:
            print(f"설정 로드 중 오류 발생: {e}")
            cls._settings = {
                "last_project": None,
                "debug_mode": False
            }
    
    @classmethod
    def save_settings(cls):
        """설정을 파일에 저장합니다."""
        try:
            settings_path = Path(cls._settings_file)
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(cls._settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"설정 저장 중 오류 발생: {e}")
    
    @classmethod
    def get(cls, key, default=None):
        """설정 값을 가져옵니다."""
        if not cls._settings:
            cls.load_settings()
        return cls._settings.get(key, default)
    
    @classmethod
    def set(cls, key, value):
        """설정 값을 저장합니다."""
        if not cls._settings:
            cls.load_settings()
        cls._settings[key] = value
        cls.save_settings()
    
    @classmethod
    def get_last_project(cls):
        """마지막 프로젝트 정보를 가져옵니다."""
        return cls.get("last_project")
    
    @classmethod
    def set_last_project(cls, project_info):
        """마지막 프로젝트 정보를 저장합니다."""
        if project_info:
            # Project 객체를 딕셔너리로 변환하여 저장
            if hasattr(project_info, 'to_dict'):
                cls.set("last_project", project_info.to_dict())
            elif isinstance(project_info, dict):
                cls.set("last_project", project_info)
            else:
                cls.set("last_project", None)
        else:
            cls.set("last_project", None)
    
    @classmethod
    def is_debug_mode(cls):
        """디버그 모드 상태를 반환합니다."""
        return cls.get("debug_mode", False)
    
    @classmethod
    def set_debug_mode(cls, enabled: bool):
        """디버그 모드를 설정합니다."""
        cls.set("debug_mode", enabled)


# 초기에 설정 로드
Settings.load_settings()
