"""
텍스트를 이미지로 변환하는 서비스
텍스트를 받아서 PIL Image로 변환하여 반환
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Optional
from utils import FontUtils


class TextImageService:
    """텍스트를 이미지로 변환하는 서비스 클래스"""
    
    @classmethod
    def create_text_image(
        cls,
        text: str,
        font_path: str = FontUtils.MAPLESTORY_LIGHT,
        font_size: int = 80,
        color: str = 'black',
        screen_size: tuple = (1080, 1920),
        text_width: int = 1080,
        position: tuple = (540, 960),
        text_align: str = "center"
    ) -> Optional[Image.Image]:
        """
        텍스트를 이미지로 변환 (캔버스 내 특정 위치에 텍스트 그리기)
        
        Args:
            text (str): 변환할 텍스트
            font_path (str): 폰트 경로 (기본값: MAPLESTORY_LIGHT)
            font_size (int): 폰트 크기 (기본값: 80)
            color (str): 텍스트 색상 (기본값: 'black')
            screen_size (tuple): 캔버스 크기 (width, height) (기본값: (1080, 1920))
            text_width (int): 텍스트 한 줄 너비 (기본값: 1080)
            position (tuple): 텍스트를 그릴 중점 위치 (x, y) (기본값: (540, 960))
            text_align (str): 텍스트 정렬 ("center", "left", "right") (기본값: "center")
        
        Returns:
            Image.Image: 생성된 이미지 객체 또는 None (실패 시)
        """
        try:
            # 이미지 생성 (투명 배경, screen_size 크기)
            img = Image.new('RGBA', screen_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 폰트 로드
            try:
                font = ImageFont.truetype(font_path, font_size)
            except Exception:
                # 폰트 로드 실패 시 기본 폰트 사용
                font = ImageFont.load_default()
            
            # 텍스트를 줄바꿈으로 분리
            lines = [line for line in text.split('\n') if line.strip()]  # 빈 줄 제거
            
            if not lines:
                return img
            
            # 각 줄의 높이 계산
            # bbox (bounding box): 텍스트가 차지하는 영역의 좌표 (left, top, right, bottom)
            # textbbox는 텍스트의 경계 상자를 반환: (left, top, right, bottom)
            bbox = draw.textbbox((0, 0), "가", font=font)  # 기준 문자로 높이 측정
            text_height = bbox[3] - bbox[1]  # bottom - top = 텍스트 높이
            
            # 줄 간격 추가 (기본값: 텍스트 높이의 20%)
            line_spacing = int(text_height * 0.4)
            line_height = text_height + line_spacing  # 줄 높이 = 텍스트 높이 + 줄 간격
            
            # 전체 텍스트 블록의 높이 계산 (마지막 줄은 줄 간격 없음)
            total_height = (len(lines) - 1) * line_height + text_height
            
            # 텍스트 위치 계산 (position을 중점으로)
            pos_x, pos_y = position
            
            # 색상 변환 (문자열을 RGB 튜플로)
            rgb_color = cls._parse_color(color)
            
            # 각 줄을 개별적으로 그리기
            for line_idx, line in enumerate(lines):
                if not line.strip():  # 빈 줄은 스킵
                    continue
                
                # 각 줄의 너비 계산
                line_bbox = draw.textbbox((0, 0), line, font=font)
                line_width = line_bbox[2] - line_bbox[0]
                
                # text_align에 따라 x 좌표 계산 (각 줄을 개별적으로 정렬)
                if text_align == "center":
                    # text_width 내에서 중앙 정렬
                    x = pos_x - (line_width // 2)
                elif text_align == "right":
                    # text_width 내에서 오른쪽 정렬
                    x = pos_x - line_width
                else:  # left
                    # text_width 내에서 왼쪽 정렬
                    x = pos_x
                
                # y 좌표 계산 (전체 텍스트 블록의 중점 기준)
                # 첫 번째 줄의 y 좌표 = position.y - (전체 높이 / 2) + (텍스트 높이 / 2)
                # 이후 줄은 line_height만큼 아래로 이동
                y = pos_y - (total_height // 2) + (line_idx * line_height) + (text_height // 2)
                
                # 텍스트 그리기
                draw.text((x, y), line, font=font, fill=rgb_color)
            
            return img
            
        except Exception as e:
            print(f"텍스트 이미지 생성 중 오류 발생: {e}")
            return None
    
    @staticmethod
    def _parse_color(color: str) -> tuple:
        """
        색상 문자열을 RGB 튜플로 변환
        
        Args:
            color (str): 색상 문자열 ('white', 'black', '#FFFFFF' 등)
        
        Returns:
            tuple: RGB 튜플 (r, g, b)
        """
        color_map = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
        }
        
        # 색상 맵에서 찾기
        if color.lower() in color_map:
            return color_map[color.lower()]
        
        # HEX 색상 처리 (#FFFFFF 형식)
        if color.startswith('#'):
            color = color[1:]
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # 기본값: 흰색
        return (255, 255, 255)


# 싱글톤 인스턴스 생성 (편의를 위해)
text_image_service = TextImageService()

