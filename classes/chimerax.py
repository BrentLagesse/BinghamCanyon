from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Union


# https://www.cgl.ucsf.edu/chimerax/docs/user/startup.html
class Chimerax:
    """Small wrapper to launch ChimeraX with a model and a Python script.

    Notes:
    - On macOS/Linux we MUST use shell=False so the model/script arguments are preserved.
    - We pass an absolute model path so ChimeraX can always locate the file.
    """

    def __init__(self, exe_path: Union[str, Path], is_window: bool = True):
        self.exe_path = str(exe_path)
        self.is_window = is_window

    def open(self, model_path: Union[str, Path]) -> None:
        model = str(Path(model_path).expanduser().resolve())
        script = str((Path("chimerax_scripts") / "automate_conservation.py").resolve())

        # ChimeraX expects scripts via --script. Any args after the script are available in sys.argv inside the script.
        cmd = [self.exe_path, "--script", script, model]

        # Do NOT use shell=True on macOS/Linux; it can drop args and you'll get an empty ChimeraX window.
        subprocess.Popen(cmd, shell=False)