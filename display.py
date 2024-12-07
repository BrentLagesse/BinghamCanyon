from pathlib import Path

import subprocess


from nicegui import app, ui
from utils import Config

from components.local_file_picker import local_file_picker


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


def run():
    chimerax = Chimerax("C:\\Program Files\\ChimeraX 1.8\\bin\chimerax.exe", True)
    chimerax.open()
    print("hello")


conf = Config.load_json("config.json")

# app.native.window_args["resizable"] = False
# app.native.start_args["debug"] = True
# app.native.settings["ALLOW_DOWNLOADS"] = True
# settings for nicegui

ui.markdown("# **Automated Conservation Tool**")
# ui.button("enlarge", on_click=run)
# ui.run(native=True, window_size=(400, 300), fullscreen=False)


async def pick_file(input: ui.input) -> None:
    result = await local_file_picker("~", multiple=False)
    ui.notify(f"You chose {result}")
    input.value = result


with ui.card():
    ui.markdown("## Settings")

    # TODO: Combine Choose file and the path into a better icon pattern https://nicegui.io/documentation/input
    with ui.row():
        exe_path_input = ui.input(
            label="ChimeraX exe path", value=conf.chimerax.exe_path
        ).classes("w-80")
        ui.button(
            "Choose file", on_click=lambda: pick_file(exe_path_input), icon="folder"
        )
    with ui.row():
        exe_path_input2 = ui.input(
            label="Jalview exe path", value=conf.jalview.exe_path
        ).classes("w-80")
        ui.button(
            "Choose file", on_click=lambda: pick_file(exe_path_input2), icon="folder"
        )

ui.separator()
ui.markdown("## Type of program")
# with ui.dropdown_button("Open me!", auto_close=True):
#     ui.item("Item 1", on_click=lambda: ui.notify("You clicked item 1"))
#     ui.item("Item 2", on_click=lambda: ui.notify("You clicked item 2"))
job_type_arr = [
    "Method 1: Yeast across all species",
    "Method 2: NOT IMPLEMENTED",
    "Method 3: NOT IMPLEMENTED",
]
with ui.card():

    toggle1 = ui.toggle(
        job_type_arr,
        value=job_type_arr[0],
    )
    # toggle2 = ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(toggle1, 'value')
    # ui.number(
    #     label="Number",
    #     value=int(conf.sequence_database.db_fetch.is_individually_retrieved)
    #     on_change=lambda e: print(e),
    # )
    ui.markdown("### Method Settings")
    # TODO: Add validation
    ui.number(
        label="Minimum Target Match (%)",
        value=conf.sequence_similarly_search.parse.target_match,
        on_change=lambda e: print(e),
    )
    ui.number(
        label="Max number of protein",
        value=conf.sequence_similarly_search.parse.max_entries,
        on_change=lambda e: print(e),
    )
    ui.button(text="Run")

# @ui.page("/")
# def index():


ui.run(dark=True)
