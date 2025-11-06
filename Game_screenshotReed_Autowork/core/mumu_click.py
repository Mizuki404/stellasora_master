import subprocess
import cv2
import numpy as np
import os
from pathlib import Path

class Tapscreen:
    def tap_screen(self, x=0, y=0, instance_num=None):
        adb_path = str(Path(r"D:\Program Files\Netease\MuMu Player 12\shell\adb.exe"))
        port = 7554 + (instance_num or 1)
        
        try:
            # 使用 capture_output=True, text=True 以确保 stdout/stderr 为 str（而非 bytes/None）
            subprocess.run(
                f'"{adb_path}" -s 127.0.0.1:{port} shell input tap {x} {y}',
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"已在坐标({x}, {y})执行点击")
            return True
        except subprocess.CalledProcessError as e:
            # 安全提取 stdout/stderr（可能为 None 或 bytes/str）
            stdout = e.stdout or ''
            stderr = e.stderr or ''
            # 如果仍然为 bytes（兼容旧代码），解码
            if isinstance(stdout, (bytes, bytearray)):
                stdout = stdout.decode('gbk', errors='ignore')
            if isinstance(stderr, (bytes, bytearray)):
                stderr = stderr.decode('gbk', errors='ignore')
            error_msg = stderr.strip() or stdout.strip() or f"returncode={getattr(e,'returncode',None)}"
            raise RuntimeError(f"点击失败: {error_msg}") from e
        
default_screenshot = Tapscreen()