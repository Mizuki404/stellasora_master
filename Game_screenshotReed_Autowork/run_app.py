"""Application bootstrap for the Stellasora Master automation suite."""
from __future__ import annotations

import importlib
import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

PYPI_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"
REQUIRED_PACKAGES = [
    "flask",
    "opencv-python",
    "numpy",
]
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000


def resource_root() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def ensure_sys_path(root: Path) -> None:
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def install_missing_packages(packages: list[str]) -> None:
    missing: list[str] = []
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ModuleNotFoundError:
            missing.append(pkg)
    if not missing:
        return

    cmd = [sys.executable, "-m", "pip", "install", "-i", PYPI_MIRROR, *missing]
    subprocess.check_call(cmd)


def find_open_port(host: str, start_port: int) -> int:
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return port
            except OSError:
                port += 1


def launch_browser(host: str, port: int) -> None:
    url = f"http://{host}:{port}/"

    def _open() -> None:
        for _ in range(12):
            time.sleep(0.5)
            try:
                with socket.create_connection((host, port), timeout=0.2):
                    webbrowser.open(url, new=2)
                    return
            except OSError:
                continue

    threading.Thread(target=_open, daemon=True).start()


def main() -> None:
    root = resource_root()
    ensure_sys_path(root)

    # Only attempt to install dependencies when not running from PyInstaller bundle.
    if not getattr(sys, "_MEIPASS", None):
        install_missing_packages(REQUIRED_PACKAGES)

    os.chdir(root)

    from webapp.app import app

    port = find_open_port(DEFAULT_HOST, DEFAULT_PORT)
    launch_browser(DEFAULT_HOST, port)
    app.run(host=DEFAULT_HOST, port=port, debug=False, threaded=True, use_reloader=False)


if __name__ == "__main__":
    main()
