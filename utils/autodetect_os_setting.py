import platform
from pathlib import Path
from typing import List
from utils.config import Config


def autodetect_os_setting(conf: Config) -> bool:
    def find_folder(root_folder: Path, find_folder_regex: str) -> List[str]:
        # NOTE: find_folder_regex isn't used right now; keeping signature to avoid refactors elsewhere.
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
        # ChimeraX
        user_dir = Path("C:\\Program Files")
        matching_chimerax_folders = find_folder(
            root_folder=user_dir, find_folder_regex="ChimeraX"
        )
        if len(matching_chimerax_folders) != 1:
            print("Cannot autodetect ChimeraX")
            return False
        chimerax_exe_path = Path(matching_chimerax_folders[0]) / "bin" / "chimerax.exe"

        # Jalview (common Windows install)
        user_dir = Path.home()
        jalview_exe_path = user_dir / "AppData" / "Local" / "Jalview" / "jalviewg.exe"

    if platform.system() == "Darwin":
        app_path = Path("/Applications")

        # ChimeraX: look for exactly one ChimeraX*.app bundle
        matching_chimerax_folders = find_folder(
            root_folder=app_path, find_folder_regex="ChimeraX"
        )
        if len(matching_chimerax_folders) != 1:
            print("Cannot autodetect ChimeraX")
            return False

        chimerax_exe_path = (
            Path(matching_chimerax_folders[0]) / "Contents" / "MacOS" / "ChimeraX"
        )

        # Jalview: internal executable name varies by version. Try common candidates.
        jalview_candidates = [
            app_path / "Jalview.app" / "Contents" / "MacOS" / "Jalview",
            app_path / "Jalview.app" / "Contents" / "MacOS" / "JavaApplicationStub",
        ]
        jalview_exe_path = next((p for p in jalview_candidates if p.exists()), None)

        if jalview_exe_path is None:
            print("Cannot autodetect Jalview (Jalview.app not found or bundle layout is different)")
            return False

    print(f"ChimeraX exe path: {chimerax_exe_path}")
    print(f"Jalview exe path: {jalview_exe_path}")
    conf.chimerax.exe_path = str(chimerax_exe_path)
    conf.jalview.exe_path = str(jalview_exe_path)
    return True