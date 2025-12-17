"""
비디오 생성 관련 유틸리티 클래스
씬들의 비디오를 생성하고 합성하는 기능을 제공합니다.
"""

from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips
from project_manager import project_manager
from ui.scene_types import get_scene_class


class VideoGenerator:
    """비디오 생성 및 합성을 담당하는 클래스"""
    
    def __init__(self):
        """VideoGenerator 초기화"""
        pass
    
    def generate_all_scene_videos(
        self,
        scenes: List[Dict[str, Any]],
        progress_callback: Optional[Callable[[float], None]] = None,
        status_callback: Optional[Callable[[str], None]] = None,
        warning_callback: Optional[Callable[[str], None]] = None
    ) -> List[str]:
        """
        모든 씬의 비디오를 생성합니다.
        
        Args:
            scenes (List[Dict[str, Any]]): 씬 정보 리스트
            progress_callback (Optional[Callable[[float], None]]): 진행률 업데이트 콜백 (0.0 ~ 1.0)
            status_callback (Optional[Callable[[str], None]]): 상태 메시지 업데이트 콜백
            warning_callback (Optional[Callable[[str], None]]): 경고 메시지 콜백
            
        Returns:
            List[str]: 생성된 비디오 파일의 전체 경로 리스트
        """
        video_paths = []
        
        for idx, scene in enumerate(scenes):
            scene_type = scene.get('type', 'type1')
            SceneClass = get_scene_class(scene_type)
            
            if SceneClass:
                # 상태 메시지 업데이트
                if status_callback:
                    status_callback(f"씬 {idx + 1}/{len(scenes)} 생성 중...")
                
                # 씬 인스턴스 생성 및 비디오 생성
                scene_instance = SceneClass(scene)
                video_path = scene_instance.generate_video_structure()
                
                if video_path:
                    # 상대 경로를 전체 경로로 변환
                    project_path = project_manager.get_project_path()
                    if project_path:
                        full_path = project_path / video_path
                        if full_path.exists():
                            video_paths.append(str(full_path))
                else:
                    # 비디오 생성 실패 경고
                    if warning_callback:
                        warning_callback(f"씬 {idx + 1}의 비디오 생성에 실패했습니다.")
            else:
                # 알 수 없는 씬 타입 경고
                if warning_callback:
                    warning_callback(f"알 수 없는 씬 타입: {scene_type}")
            
            # 진행률 업데이트
            if progress_callback:
                progress_callback((idx + 1) / len(scenes))
        
        return video_paths
    
    def concatenate_videos(
        self,
        video_paths: List[str],
        output_filename: str = "final_output.mp4",
        status_callback: Optional[Callable[[str], None]] = None,
        error_callback: Optional[Callable[[str], None]] = None
    ) -> Optional[str]:
        """
        여러 비디오 파일을 하나로 합성합니다.
        
        Args:
            video_paths (List[str]): 합성할 비디오 파일 경로 리스트
            output_filename (str): 출력 파일명 (기본값: "final_output.mp4")
            status_callback (Optional[Callable[[str], None]]): 상태 메시지 업데이트 콜백
            error_callback (Optional[Callable[[str], None]]): 에러 메시지 콜백
            
        Returns:
            Optional[str]: 생성된 비디오 파일의 전체 경로 또는 None (실패 시)
        """
        if not video_paths:
            if error_callback:
                error_callback("합성할 비디오가 없습니다.")
            return None
        
        try:
            # 상태 메시지 업데이트
            if status_callback:
                status_callback("비디오 합치는 중...")
            
            # 비디오 클립 로드
            clips = [VideoFileClip(path) for path in video_paths]
            
            # 비디오 합성
            final_video = concatenate_videoclips(clips)
            
            # 전체 비디오 저장
            project_path = project_manager.get_project_path()
            if not project_path:
                if error_callback:
                    error_callback("프로젝트 경로를 찾을 수 없습니다.")
                return None
            
            output_path = project_path / "output" / output_filename
            final_video.write_videofile(str(output_path), fps=24)
            
            # 리소스 정리
            final_video.close()
            for clip in clips:
                clip.close()
            
            return str(output_path)
            
        except Exception as e:
            if error_callback:
                error_callback(f"비디오 합치기 중 오류 발생: {e}")
            return None
    
    def generate_final_video(
        self,
        scenes: List[Dict[str, Any]],
        output_filename: str = "final_output.mp4",
        progress_callback: Optional[Callable[[float], None]] = None,
        status_callback: Optional[Callable[[str], None]] = None,
        warning_callback: Optional[Callable[[str], None]] = None,
        error_callback: Optional[Callable[[str], None]] = None,
        success_callback: Optional[Callable[[str], None]] = None
    ) -> Optional[str]:
        """
        모든 씬의 비디오를 생성하고 합성하여 최종 비디오를 만듭니다.
        
        Args:
            scenes (List[Dict[str, Any]]): 씬 정보 리스트
            output_filename (str): 출력 파일명 (기본값: "final_output.mp4")
            progress_callback (Optional[Callable[[float], None]]): 진행률 업데이트 콜백 (0.0 ~ 1.0)
            status_callback (Optional[Callable[[str], None]]): 상태 메시지 업데이트 콜백
            warning_callback (Optional[Callable[[str], None]]): 경고 메시지 콜백
            error_callback (Optional[Callable[[str], None]]): 에러 메시지 콜백
            success_callback (Optional[Callable[[str], None]]): 성공 메시지 콜백
            
        Returns:
            Optional[str]: 생성된 최종 비디오 파일의 전체 경로 또는 None (실패 시)
        """
        # 모든 씬의 비디오 생성
        video_paths = self.generate_all_scene_videos(
            scenes=scenes,
            progress_callback=progress_callback,
            status_callback=status_callback,
            warning_callback=warning_callback
        )
        
        if not video_paths:
            if error_callback:
                error_callback("생성된 비디오가 없습니다.")
            return None
        
        # 비디오 합성
        final_path = self.concatenate_videos(
            video_paths=video_paths,
            output_filename=output_filename,
            status_callback=status_callback,
            error_callback=error_callback
        )
        
        if final_path and success_callback:
            success_callback(f"전체 비디오 생성 완료: {final_path}")
        
        return final_path


# 전역 VideoGenerator 인스턴스
video_generator = VideoGenerator()

