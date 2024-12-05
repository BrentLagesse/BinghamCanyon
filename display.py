from pathlib import Path

import subprocess


from nicegui import app, ui


class Chimerax:
    #     """To do: handle different OS"""

    #     exe_path: str
    #     is_window: bool

    def __init__(self, exe_path: Path, is_window=True):

        # os_name = platform.system()
        # if platform.system == 'Linux' :
        #     exe_path =
        # if platform.system == 'Windows' :
        #     exe_path =
        # if platform.system == 'Darwin' :
        #     exe_path =
        self.exe_path = exe_path
        self.is_window = is_window

    def open(self, model_path: str = ""):
        # if model_path == '':
        # model = Path().resolve() / model_path
        # subprocess.Popen([self.exe_path, model], shell=self.is_window)
        # path = Path().resolve() / "chimerax_scripts" / "test.py"
        path = Path("chimerax_scripts") / "test.py"
        print(path)
        model_path = Path().resolve() / "output" / "test.cif"
        python_script = str(path)
        model_path = Path().resolve() / "output" / "test.cif"
        # fasta_format = Path().resolve() / "test" / sss_fasta_format
        # 'C:\\Users\\chhor\\Downloads\\test_clustal.aln'
        print(model_path)
        # run(session, "hello")
        # subprocess.Popen(
        #     [self.exe_path, "--script", python_script],
        #     shell=self.is_window,
        # )
        subprocess.Popen(
            [self.exe_path, model_path, python_script],
            shell=self.is_window,
        )


import time


def run():
    start = time.time()
    print(start)

    chimerax = Chimerax("C:\\Program Files\\ChimeraX 1.8\\bin\chimerax.exe", True)
    chimerax.open()
    end = time.time()
    print(end)
    print(end - start)
    print("hello")


app.native.window_args["resizable"] = False
app.native.start_args["debug"] = True
app.native.settings["ALLOW_DOWNLOADS"] = True

ui.label("app running in native mode")
ui.button("enlarge", on_click=run)

ui.run(native=True, window_size=(400, 300), fullscreen=False)
