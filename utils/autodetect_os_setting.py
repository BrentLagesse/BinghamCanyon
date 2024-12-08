import platform
from pathlib import Path

from config import Config


def autodetect_os_setting(config: Config):
    # TODO: Add Linux support
    if platform.system == "Linux":
        raise Exception("LINUX NOT YET SUPPORTED")
    if platform.system == "Windows":
        user_dir = Path.home()
        config.chimerax.exe_path = user_dir / "ChimeraX 1.8" / "bin" / "chimerax.exe"
        config.jalview.exe_path = (
            user_dir / "AppData" / "Local" / "Jalview" / "jalviewg.exe"
        )
    if platform.system == "Darwin":
        config.chimerax.exe_path = (
            "Applications/ChimeraX-1.9-rc2024.12.03.app/Contents/MacOS/ChimeraX"
        )
        config.jalview.exe_path = (
            "/Applications/Jalview.app/Contents/MacOS/JavaApplicationStub"
        )
