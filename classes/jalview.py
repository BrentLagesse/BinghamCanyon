from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Union


class Jalview:
    """Small wrapper to launch Jalview.

    On macOS/Linux, shell=False is the most reliable way to preserve arguments.
    """

    def __init__(self, exe_path: Union[str, Path], is_window: bool = True):
        self.exe_path = str(exe_path)
        self.is_window = is_window

    def open(self, ebi_url_or_path: str = "") -> None:
        # Example URL:
        # https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/<jobid>/aln-clustal_num
        subprocess.Popen([self.exe_path, ebi_url_or_path], shell=False)