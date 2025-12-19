import streamlit as st
from pathlib import Path
from service.video_manager import video_manager
from ui.popup.scene_type_dialog import scene_type_dialog
from ui.popup.video_player_popup import video_player_dialog
from project_manager import project_manager
from utils.folder_utils import open_folder_in_explorer

def show():
    
    # + 버튼과 비디오 생성 버튼, output 폴더 열기 버튼
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        if st.button("➕", width="stretch", help="새 씬 추가"):
            # 팝업 다이얼로그 열기
            scene_type_dialog()
    
    with col2:
        if st.button("🎬", width="stretch", help="비디오 생성"):
            # 비디오 생성 처리
            video_data = video_manager.get_video_data()
            scenes = video_data.get("scenes", [])
            
            if not scenes:
                st.warning("생성할 씬이 없습니다.")
            else:
                # VideoGenerator를 사용하여 비디오 생성
                from service.video_generator import video_generator
                
                # UI 요소 생성
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 콜백 함수 정의
                def update_progress(progress: float):
                    """진행률 업데이트 콜백"""
                    progress_bar.progress(progress)
                
                def update_status(status: str):
                    """상태 메시지 업데이트 콜백"""
                    status_text.text(status)
                
                def show_warning(message: str):
                    """경고 메시지 콜백"""
                    st.warning(message)
                
                def show_error(message: str):
                    """에러 메시지 콜백"""
                    st.error(message)
                
                def show_success(message: str):
                    """성공 메시지 콜백"""
                    # st.success(message)
                    status_text.text("완료!")
                
                # 최종 비디오 생성
                final_path = video_generator.generate_final_video(
                    scenes=scenes,
                    progress_callback=update_progress,
                    status_callback=update_status,
                    warning_callback=show_warning,
                    error_callback=show_error,
                    success_callback=show_success
                )
                
                # UI 요소 정리
                progress_bar.empty()
                if not final_path:
                    status_text.empty()
    
    with col3:
        # output 폴더 열기 버튼
        if st.button("📁", width="stretch", help="output 폴더 열기"):
            # 프로젝트 경로 가져오기
            project_path = project_manager.get_project_path()
            if project_path:
                # output 폴더 경로
                output_folder = project_path / "output"
                
                # utils의 폴더 열기 함수 사용
                success = open_folder_in_explorer(output_folder, bring_to_front=True)
                if not success:
                    st.error("폴더 열기에 실패했습니다.")
            else:
                st.warning("프로젝트가 로드되지 않았습니다.")
    
    # 현재 씬 목록 표시
    video_data = video_manager.get_video_data()
    scenes = video_data.get("scenes", [])
    
    if scenes:
        # 씬 타입별 클래스 가져오기 (재로드 문제 방지를 위해 함수 내부에서 import)
        from ui.scene_types import get_scene_class
        
        for idx, scene in enumerate(scenes, 1):
            scene_type = scene.get('type', 'type1')
            scene_id = scene.get('id')
            
            # 비디오 파일 존재 여부 확인
            output_folder, output_path, relative_path = project_manager.get_output_path(scene_id)
            video_exists = output_path and output_path.exists()
            
            # 씬 헤더와 비디오 생성 버튼, 재생 버튼, 삭제 버튼을 나란히 배치
            col_header, col_video, col_play, col_delete = st.columns([6, 1, 1, 1])
            
            with col_header:
                # 씬 헤더 표시
                st.markdown(f"### 씬 {idx} (Type: {scene_type})")
            
            with col_video:
                # 비디오 생성 버튼 (이 씬만)
                if st.button("🎬", key=f"video_{scene_id}", help="이 씬만 비디오 생성"):
                    # 해당 씬의 비디오 생성
                    SceneClass = get_scene_class(scene_type)
                    if SceneClass:
                        scene_instance = SceneClass(scene)
                        video_path = scene_instance.generate_video_structure()
                        
                        if not video_path:
                            st.error("비디오 생성에 실패했습니다.")
                        else:
                            # 비디오 생성 후 페이지 새로고침하여 재생 버튼 표시
                            st.rerun()
                    else:
                        st.warning(f"알 수 없는 씬 타입: {scene_type}")
            
            with col_play:
                # 비디오 파일이 있으면 재생 버튼 표시
                if video_exists:
                    if st.button("▶️", key=f"play_btn_{scene_id}", help="비디오 재생"):
                        # 비디오 재생 팝업 열기
                        scene_title = f"씬 {idx} (Type: {scene_type})"
                        video_player_dialog(output_path, scene_title)
            
            with col_delete:
                # 삭제 버튼 (X 표시)
                if st.button("❌", key=f"delete_{scene_id}", help="씬 삭제"):
                    if video_manager.remove_scene(scene_id):
                        st.success("씬이 삭제되었습니다.")
                        st.rerun()
                    else:
                        st.error("씬 삭제에 실패했습니다.")
            
            # 씬 타입에 따라 해당하는 클래스 인스턴스 생성 및 렌더링
            SceneClass = get_scene_class(scene_type)
            if SceneClass:
                scene_instance = SceneClass(scene)
                scene_instance.render()
            else:
                # 알 수 없는 타입인 경우 기본 UI 표시
                st.warning(f"알 수 없는 씬 타입: {scene_type}")
                st.json(scene)
            
            # 씬 사이 구분선 (마지막 씬이 아니면)
            if idx < len(scenes):
                st.divider()
    else:
        st.info("추가된 씬이 없습니다. + 버튼을 눌러 씬을 추가하세요.")
