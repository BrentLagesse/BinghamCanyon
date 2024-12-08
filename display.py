from pathlib import Path
import threading
import time
import subprocess

from main import jalview, chimerax


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

def open_jalview(jalview_url):
    jalview.open(jalview_url)

def open_chimerax(model_path):
    chimerax.open(model_path)

def run_main():
    try:
        # stdout redirected to subprocess pipe
        process = subprocess.Popen(
            ['python3', 'main.py'],
            stderr=subprocess.PIPE,
            text=True
            )
        ui.notify("Job recieved!")
        with ui.card():
            job_id_text = ui.label("Job ID: ").classes('text-blue-500')
            spinner = ui.spinner(size='lg')
            with ui.row() as myrow:
                pass
        

        def monitor_process():
            # Print out the job ID
            job_id = None
            jalview_url = None
            model_path = None
            for line in iter(process.stderr.readline, ''):
                if ("JOB ID: " in line):
                    job_id = line.split(":")[1].strip()
                    job_id_text.set_text(f"Job ID: {job_id}")
                # if ("JALVIEW URL: " in line):
                #     jalview_url = line.split(":")[1].strip()
                #     ui.notify(f"Jalview URL: {jalview_url}")
                # if ("MODEL PATH: " in line):
                #     model_path = line.split(":")[1].strip()
                #     ui.notify(f"Model Path: {model_path}")

            #wait for process to finish
            process.stderr.close()
            process.wait()

            print("process complete")
            # When done, print two buttons to open Jalview and ChimeraX

            # if process.returncode == 0:
            spinner.delete()
            with myrow:
                    ui.button(text="Open Jalview", on_click=lambda: open_jalview(jalview_url))
                    ui.button(text="Open ChimeraX", on_click=lambda: open_chimerax(model_path))

        
        threading.Thread(target=monitor_process, daemon=True).start()

    except Exception as e:
        ui.notify(f"Error: {e}")


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
    ui.button(text="Run", on_click=run_main)

# @ui.page("/")
# def index():


ui.run(dark=True)
