import streamlit as st

def show():
    st.title("페이지 3")
    st.markdown("이것은 세 번째 페이지입니다.")
    
    st.write("여기에 페이지 3의 내용이 표시됩니다.")
    
    # 간단한 예제 콘텐츠
    st.subheader("⚙️ 페이지 3 설정")
    st.write("- 기능: 시스템 설정")
    st.write("- 구성 요소: 8개")
    st.write("- 상태: 정상 작동")
    
    # 간단한 토글 버튼
    st.subheader("설정 옵션")
    enable_notifications = st.toggle("알림 활성화", value=True)
    enable_dark_mode = st.toggle("다크 모드", value=False)
    auto_save = st.toggle("자동 저장", value=True)
    
    st.write(f"알림: {'활성화' if enable_notifications else '비활성화'}")
    st.write(f"다크 모드: {'활성화' if enable_dark_mode else '비활성화'}")
    st.write(f"자동 저장: {'활성화' if auto_save else '비활성화'}")
    
    # 간단한 슬라이더
    st.subheader("기타 설정")
    refresh_rate = st.slider("새로고침 주기 (초)", 1, 60, 5)
    st.write(f"새로고침 주기: {refresh_rate}초")
