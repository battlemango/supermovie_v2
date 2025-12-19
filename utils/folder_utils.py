"""
폴더 관련 유틸리티 함수
Windows 탐색기에서 폴더를 열고 최상위로 가져오는 기능 제공
"""
import os
import subprocess
import time
import ctypes
from pathlib import Path
from typing import Optional


def bring_explorer_to_front():
    """
    Windows에서 탐색기 창을 찾아서 최상위로 가져오기
    
    탐색기 창을 찾아서 포커스를 주고 최상위로 가져옵니다.
    """
    try:
        # Windows API 상수 정의
        SW_RESTORE = 9
        explorer_windows = []
        
        # 모든 창을 순회하며 탐색기 창 찾기
        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        def enum_windows_proc(hwnd, lParam):
            """창 열거 콜백 함수"""
            if ctypes.windll.user32.IsWindowVisible(hwnd):
                class_name = ctypes.create_unicode_buffer(256)
                ctypes.windll.user32.GetClassNameW(hwnd, class_name, 256)
                
                # 탐색기 창인지 확인 (CabinetWClass 또는 ExploreWClass)
                if "CabinetWClass" in class_name.value or "ExploreWClass" in class_name.value:
                    explorer_windows.append(hwnd)
            return True
        
        # 모든 창 열거
        ctypes.windll.user32.EnumWindows(enum_windows_proc, 0)
        
        # 찾은 탐색기 창 중 가장 최근 것(마지막)을 최상위로 가져오기
        if explorer_windows:
            hwnd = explorer_windows[-1]
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
            ctypes.windll.user32.BringWindowToTop(hwnd)
    except Exception:
        # Windows API 호출 실패 시 무시 (다른 OS에서도 작동하도록)
        pass


def open_folder_in_explorer(folder_path: Path, bring_to_front: bool = True) -> bool:
    """
    Windows 탐색기에서 폴더를 열고 최상위로 가져오기
    
    Args:
        folder_path (Path): 열 폴더 경로
        bring_to_front (bool): 창을 최상위로 가져올지 여부 (기본값: True)
    
    Returns:
        bool: 성공 여부
    """
    try:
        # 폴더가 없으면 생성
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # subprocess를 사용하여 explorer.exe를 실행
        subprocess.Popen(
            ['explorer.exe', str(folder_path)],
            shell=False
        )
        
        # 창이 열릴 시간을 확보하기 위해 잠시 대기
        if bring_to_front:
            time.sleep(0.3)
            # Windows에서 탐색기 창을 최상위로 가져오기
            bring_explorer_to_front()
        
        return True
        
    except Exception as e:
        # subprocess가 실패하면 os.startfile로 대체 시도
        try:
            os.startfile(str(folder_path))
            if bring_to_front:
                time.sleep(0.3)
                bring_explorer_to_front()
            return True
        except Exception as e2:
            # 모든 방법 실패
            print(f"폴더 열기 실패: {str(e2)}")
            return False

