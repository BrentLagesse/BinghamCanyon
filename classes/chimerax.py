from pathlib import Path

import subprocess

# https://www.cgl.ucsf.edu/chimerax/docs/user/startup.html#:~:text=ChimeraX%20can%20be%20started%20from,executable%20created%20by%20the%20installer.
class Chimerax():
    """To do: handle different OS"""
    exe_path : str
    is_window : bool
    def __init__(self, exe_path :Path, is_window = True):
        self.exe_path = exe_path
        self.is_window = is_window
        
    def open(self, model_path :str = ''):
        # if model_path == '':
        model = Path().resolve() / model_path
        subprocess.Popen([self.exe_path, model], shell = self.is_window)


# "Program Files\ChimeraX 1.8\bin\chimerax.exe" --stereo --start
