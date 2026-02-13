from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Union, Optional


# https://www.cgl.ucsf.edu/chimerax/docs/user/startup.html
class Chimerax:
    """Small wrapper to launch ChimeraX with a model and (optionally) an alignment file.

    Notes:
    - On macOS/Linux we MUST use shell=False so the model/script arguments are preserved.
    - We pass absolute paths so ChimeraX can always locate the files.
    - Any args after the script are available in sys.argv inside the script.
      Example:
        sys.argv[1] -> model path
        sys.argv[2] -> alignment path (if provided)
    """

    def __init__(self, exe_path: Union[str, Path], is_window: bool = True):
        self.exe_path = str(exe_path)
        self.is_window = is_window

    def open(self, model_path: Union[str, Path], aln_path: Optional[Union[str, Path]] = None) -> None:
        model = str(Path(model_path).expanduser().resolve())
        script = str((Path("chimerax_scripts") / "automate_conservation.py").resolve())

        # ChimeraX expects scripts via --script. Any args after the script are available in sys.argv inside the script.
        cmd = [self.exe_path, "--script", script, model]

        # Optional: pass alignment path as argv[2]
        if aln_path is not None:
            cmd.append(str(Path(aln_path).expanduser().resolve()))

        # Do NOT use shell=True on macOS/Linux; it can drop args and you'll get an empty ChimeraX window.
        subprocess.Popen(cmd, shell=False)