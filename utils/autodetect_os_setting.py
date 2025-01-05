import platform
from pathlib import Path
from typing import List
from utils.config import Config


def autodetect_os_setting(conf: Config) -> bool:
    def find_folder(root_folder: Path, find_folder_regex: str) -> List[str]:
        matching_folders = [
            str(folder)
            for folder in root_folder.iterdir()
            if folder.is_dir() and "ChimeraX" in folder.name
        ]
        return matching_folders

    chimerax_exe_path: Path
    jalview_exe_path: Path
    print("Autodetecting os settings")
    print("User's OS is ", platform.system())
    # TODO: Add Linux support
    if platform.system() == "Linux":
        raise Exception("LINUX NOT YET SUPPORTED")
    if platform.system() == "Windows":
        # Chimerax
        user_dir = Path("C:\\Program Files")
        matching_chimerax_folders = find_folder(
            root_folder=user_dir, find_folder_regex="ChimeraX"
        )
        if len(matching_chimerax_folders) != 1:
            print("Cannot autodetect ChimeraX")
            return False
        # TODO: automatically checks if this file exist and give the user worrying that its not working
        chimerax_exe_path = Path(matching_chimerax_folders[0]) / "bin" / "chimerax.exe"
        # Jalview
        # Ex. Path.home() = C:\\Users\\chhor
        user_dir = Path.home()
        jalview_exe_path = user_dir / "AppData" / "Local" / "Jalview" / "jalviewg.exe"
        print(jalview_exe_path)
    if platform.system() == "Darwin":
        app_path = Path("/Applications")
        matching_chimerax_folders = find_folder(
            root_folder=app_path, find_folder_regex="ChimeraX"
        )
        if len(matching_chimerax_folders) != 1:
            print("Cannot autodetect ChimeraX")
            return False
        chimerax_exe_path = (
            Path(matching_chimerax_folders[0]) / "Contents" / "MacOS" / "ChimeraX"
        )
        jalview_exe_path = (
            app_path / "Jalview.app" / "Contents" / "MacOS" / "JavaApplicationStub"
        )
        # Example of what macs path would look like
        # config.chimerax.exe_path = (
        #     "Applications/ChimeraX-1.9-rc2024.12.03.app/Contents/MacOS/ChimeraX"
        # )
        # config.jalview.exe_path = (
        #     "/Applications/Jalview.app/Contents/MacOS/JavaApplicationStub"
        # )
    print(f"ChimeraX exe path: {chimerax_exe_path}")
    print(f"Jalview exe path: {jalview_exe_path}")
    conf.chimerax.exe_path = str(chimerax_exe_path)
    conf.jalview.exe_path = str(jalview_exe_path)
    return True
