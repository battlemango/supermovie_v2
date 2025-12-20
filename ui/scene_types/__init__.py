"""
씬 타입별 UI 모듈
각 타입에 맞는 UI를 제공하는 모듈들을 포함합니다.
"""

from ui.scene_types.dimango_end_type import DimangoEndType
from ui.scene_types.dimango_type import DimangoType
from ui.scene_types.type1 import Type1Scene
from ui.scene_types.type2 import Type2Scene
from ui.scene_types.type3 import Type3Scene
from ui.scene_types.balance_christmas_main import BalanceChristmasMain
from ui.scene_types.balance_christmas_enter import BalanceChristmasEnter
from ui.scene_types.balance_christmas_exit import BalanceChristmasExit

__all__ = ['Type1Scene', 'Type2Scene', 'Type3Scene', 'BalanceChristmasMain', 'BalanceChristmasEnter', 'BalanceChristmasExit', 'get_scene_class', 'scene_classes']

# 씬 타입 정보: (클래스, 표시 이름)
scene_classes = {
    "type1": (Type1Scene, "Type 1"),
    "type2": (Type2Scene, "Type 2"),
    "type3": (Type3Scene, "Type 3"),
    "balance_christmas_main": (BalanceChristmasMain, "Balance Christmas Main"),
    "balance_christmas_enter": (BalanceChristmasEnter, "Balance Christmas Enter"),
    "balance_christmas_exit": (BalanceChristmasExit, "Balance Christmas Exit"),
    "dimango_type": (DimangoType, "Dimango Type"),
    "dimango_end_type": (DimangoEndType, "Dimango End Type")
}


def get_scene_class(scene_type: str):
    """
    씬 타입에 맞는 클래스 반환
    
    Args:
        scene_type (str): 씬 타입 ("type1", "type2", "type3", "balance_christmas_main" 등)
        
    Returns:
        BaseSceneType: 해당 타입의 씬 클래스 또는 None
    """
    scene_info = scene_classes.get(scene_type)
    return scene_info[0] if scene_info else None


def get_scene_display_name(scene_type: str):
    """
    씬 타입의 표시 이름 반환
    
    Args:
        scene_type (str): 씬 타입
        
    Returns:
        str: 표시 이름 또는 None
    """
    scene_info = scene_classes.get(scene_type)
    return scene_info[1] if scene_info else None
