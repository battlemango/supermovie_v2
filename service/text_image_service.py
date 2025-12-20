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
        color: str = 'white',
        size: tuple = (1080, 1920),
        margin: tuple = (0, 0),
        text_align: str = "center"
    ) -> Optional[Image.Image]:
        """
        텍스트를 이미지로 변환
        
        Args:
            text (str): 변환할 텍스트
            font_path (str): 폰트 경로 (기본값: MAPLESTORY_LIGHT)
            font_size (int): 폰트 크기 (기본값: 80)
            color (str): 텍스트 색상 (기본값: 'white')
            size (tuple): 이미지 크기 (width, height) (기본값: (1080, 1920))
            margin (tuple): 여백 (x, y) (기본값: (0, 0))
            text_align (str): 텍스트 정렬 ("center", "left", "right") (기본값: "center")
        
        Returns:
            Image.Image: 생성된 이미지 객체 또는 None (실패 시)
        """
        try:
            # 이미지 생성 (투명 배경)
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 폰트 로드
            try:
                font = ImageFont.truetype(font_path, font_size)
            except Exception:
                # 폰트 로드 실패 시 기본 폰트 사용
                font = ImageFont.load_default()
            
            # 텍스트 크기 계산
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 텍스트 위치 계산
            width, height = size
            margin_x, margin_y = margin
            
            if text_align == "center":
                x = (width - text_width) // 2 + margin_x
            elif text_align == "right":
                x = width - text_width - margin_x
            else:  # left
                x = margin_x
            
            y = margin_y
            
            # 색상 변환 (문자열을 RGB 튜플로)
            rgb_color = cls._parse_color(color)
            
            # 텍스트 그리기
            draw.text((x, y), text, font=font, fill=rgb_color)
            
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

