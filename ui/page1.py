import streamlit as st
from service.video_manager import video_manager

def show():
    st.title("페이지 1")
    st.markdown("이것은 첫 번째 페이지입니다.")
    
    st.write("여기에 페이지 1의 내용이 표시됩니다.")
    
    # 간단한 예제 콘텐츠
    st.subheader("📋 페이지 1 정보")
    st.write("- 기능: 기본 정보 표시")
    st.write("- 상태: 활성")
    st.write("- 마지막 업데이트: 2025-12-16")
    
    # + 버튼으로 씬 추가
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕", use_container_width=True, help="새 씬 추가"):
            # video_manager의 add_scene 함수 호출
            new_scene = video_manager.add_scene()
            if new_scene:
                st.success(f"씬이 추가되었습니다! (ID: {new_scene['id'][:8]}...)")
                st.rerun()
            else:
                st.error("프로젝트를 먼저 로드해주세요.")
    
    # 현재 씬 목록 표시
    video_data = video_manager.get_video_data()
    scenes = video_data.get("scenes", [])
    
    if scenes:
        st.subheader("📹 씬 목록")
        for idx, scene in enumerate(scenes, 1):
            st.write(f"{idx}. {scene.get('text', 'N/A')} (ID: {scene.get('id', 'N/A')[:8]}...)")
    else:
        st.info("추가된 씬이 없습니다. + 버튼을 눌러 씬을 추가하세요.")
    
    # 간단한 입력 필드
    st.text_input("페이지 1 입력", placeholder="여기에 입력하세요...")
