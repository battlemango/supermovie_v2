"""
씬 타입별 UI 모듈
각 타입에 맞는 UI를 제공하는 모듈들을 포함합니다.
"""

from ui.scene_types.type1 import Type1Scene
from ui.scene_types.type2 import Type2Scene
from ui.scene_types.type3 import Type3Scene

__all__ = ['Type1Scene', 'Type2Scene', 'Type3Scene', 'get_scene_class']


def get_scene_class(scene_type: str):
    """
    씬 타입에 맞는 클래스 반환
    
    Args:
        scene_type (str): 씬 타입 ("type1", "type2", "type3" 등)
        
    Returns:
        BaseSceneType: 해당 타입의 씬 클래스 또는 None
    """
    scene_classes = {
        "type1": Type1Scene,
        "type2": Type2Scene,
        "type3": Type3Scene
    }
    return scene_classes.get(scene_type)

