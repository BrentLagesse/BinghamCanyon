from pathlib import Path
import subprocess

class Jalview():
    
    """To do: handle different OS"""
    exe_path : str
    is_window : bool
    def __init__(self, exe_path :Path, is_window = True):
        self.exe_path = exe_path
        self.is_window = is_window
        # run(['jalview_exe_path', "https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/clustalo-R20240709-165430-0694-644924-p1m/aln-clustal_num"], shell = True)
        
    def open(self, ebi_url :str = ''):
        subprocess.Popen([self.exe_path, ebi_url], shell = self.is_window)
        