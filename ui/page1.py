import streamlit as st
from service.video_manager import video_manager

@st.dialog("씬 타입 선택")
def scene_type_dialog():
    """씬 타입을 선택하는 팝업 다이얼로그"""
    st.write("씬의 타입을 선택하세요")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Type 1", use_container_width=True, type="primary"):
            # type1으로 씬 추가
            new_scene = video_manager.add_scene(scene_type="type1")
            if new_scene:
                st.success(f"씬이 추가되었습니다! (Type: type1)")
                st.rerun()
            else:
                st.error("프로젝트를 먼저 로드해주세요.")
    
    with col2:
        if st.button("Type 2", use_container_width=True, type="primary"):
            # type2로 씬 추가
            new_scene = video_manager.add_scene(scene_type="type2")
            if new_scene:
                st.success(f"씬이 추가되었습니다! (Type: type2)")
                st.rerun()
            else:
                st.error("프로젝트를 먼저 로드해주세요.")
    
    with col3:
        if st.button("Type 3", use_container_width=True, type="primary"):
            # type3으로 씬 추가
            new_scene = video_manager.add_scene(scene_type="type3")
            if new_scene:
                st.success(f"씬이 추가되었습니다! (Type: type3)")
                st.rerun()
            else:
                st.error("프로젝트를 먼저 로드해주세요.")
    
    # 닫기 버튼
    st.divider()
    if st.button("취소", use_container_width=True):
        st.rerun()

def show():
    
    # + 버튼과 비디오 생성 버튼
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("➕", use_container_width=True, help="새 씬 추가"):
            # 팝업 다이얼로그 열기
            scene_type_dialog()
    
    with col2:
        if st.button("🎬", use_container_width=True, help="비디오 생성"):
            # 비디오 생성 처리
            video_data = video_manager.get_video_data()
            scenes = video_data.get("scenes", [])
            
            if not scenes:
                st.warning("생성할 씬이 없습니다.")
            else:
                # 각 씬의 비디오 생성
                from ui.scene_types import get_scene_class
                from moviepy import VideoFileClip, concatenate_videoclips
                from project_manager import project_manager
                from pathlib import Path
                
                video_paths = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 각 씬의 비디오 생성
                for idx, scene in enumerate(scenes):
                    scene_type = scene.get('type', 'type1')
                    SceneClass = get_scene_class(scene_type)
                    
                    if SceneClass:
                        status_text.text(f"씬 {idx + 1}/{len(scenes)} 생성 중...")
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
                            st.warning(f"씬 {idx + 1}의 비디오 생성에 실패했습니다.")
                    else:
                        st.warning(f"알 수 없는 씬 타입: {scene_type}")
                    
                    progress_bar.progress((idx + 1) / len(scenes))
                
                # 모든 씬의 비디오를 concat하여 전체 영상 생성
                if video_paths:
                    try:
                        status_text.text("비디오 합치는 중...")
                        clips = [VideoFileClip(path) for path in video_paths]
                        final_video = concatenate_videoclips(clips)
                        
                        # 전체 비디오 저장
                        project_path = project_manager.get_project_path()
                        if project_path:
                            output_path = project_path / "output" / "final_output.mp4"
                            final_video.write_videofile(str(output_path), fps=24)
                            
                            # 리소스 정리
                            final_video.close()
                            for clip in clips:
                                clip.close()
                            
                            st.success(f"전체 비디오 생성 완료: {output_path}")
                            status_text.text("완료!")
                        else:
                            st.error("프로젝트 경로를 찾을 수 없습니다.")
                    except Exception as e:
                        st.error(f"비디오 합치기 중 오류 발생: {e}")
                else:
                    st.warning("생성된 비디오가 없습니다.")
                
                progress_bar.empty()
                status_text.empty()
    
    # 현재 씬 목록 표시
    video_data = video_manager.get_video_data()
    scenes = video_data.get("scenes", [])
    
    if scenes:
        # 씬 타입별 클래스 가져오기 (재로드 문제 방지를 위해 함수 내부에서 import)
        from ui.scene_types import get_scene_class
        
        for idx, scene in enumerate(scenes, 1):
            scene_type = scene.get('type', 'type1')
            scene_id = scene.get('id')
            
            # 씬 헤더와 삭제 버튼, 비디오 생성 버튼을 나란히 배치
            col_header, col_video, col_delete = st.columns([8, 1, 1
            ])
            
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
                        
                        if video_path:
                            st.success(f"비디오 생성 완료: {video_path}")
                        else:
                            st.error("비디오 생성에 실패했습니다.")
                    else:
                        st.warning(f"알 수 없는 씬 타입: {scene_type}")
            
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
    
