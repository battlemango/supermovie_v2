# MoviePy 2.x 버전에서는 moviepy.editor가 제거되었습니다
# 이제 moviepy에서 직접 import합니다
from moviepy import TextClip

# 텍스트 클립 생성 (MoviePy 2.x에서는 text, font_size 파라미터 사용)
txt_clip = TextClip(text="Hello World", font_size=70, color='white', duration=3)

# 비디오 저장 (fps 지정 필요)
output_path = "output.mp4"
txt_clip.write_videofile(output_path, fps=24)
print(f"텍스트 비디오 저장 완료: {output_path}")