"""
씬 타입별 UI 모듈
각 타입에 맞는 UI를 제공하는 모듈들을 포함합니다.
"""

from ui.scene_types.type1 import render_type1
from ui.scene_types.type2 import render_type2
from ui.scene_types.type3 import render_type3

__all__ = ['render_type1', 'render_type2', 'render_type3']

