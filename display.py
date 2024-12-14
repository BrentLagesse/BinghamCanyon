from pathlib import Path
import threading
import time
from subprocess import Popen, PIPE, STDOUT

from typing import List
from functools import reduce
from nicegui import app, ui, native
from nicegui.events import ValueChangeEventArguments
from utils.config import ConfigManager, Config
from utils.autodetect_os_setting import autodetect_os_setting
from components.local_file_picker import local_file_picker
from constants import OUTPUT_FOLDER_PATH, RESULT_NAME, CONFIG_NAME
import sys
import uuid
from classes import Chimerax, Jalview

# TODO: Clean up this whole file and separate the the UI components to their own file and import them here so its not that long

config_man = ConfigManager(Path("config.json"))


ui.markdown("# **Automated Conservation Tool**")


async def pick_file(input: ui.input) -> None:
    result = await local_file_picker("~", multiple=False)
    ui.notify(f"You chose {result}")
    input.value = result


def open_jalview(jalview_url: str, job_id: str):
    # Should probably just read the settings value in the webpage
    job_conf_path = Path(OUTPUT_FOLDER_PATH / job_id / CONFIG_NAME)
    job_conf = Config().load_json(str(job_conf_path))
    jalview = Jalview(
        exe_path=job_conf.jalview.exe_path,
        is_window=True,
    )
    jalview.open(jalview_url)


def open_chimerax(model_path, job_id: str):
    # Should probably just read the settings value in the webpage
    job_conf_path = Path(OUTPUT_FOLDER_PATH / job_id / CONFIG_NAME)
    job_conf = Config().load_json(str(job_conf_path))
    chimerax = Chimerax(exe_path=job_conf.chimerax.exe_path, is_window=True)
    chimerax.open(model_path)


def run_main(uniprot_entry: str):
    # TODO: ERROR CHECKING
    if uniprot_entry == "":
        ui.notification(
            message="Uniprot entry is empty",
            type="negative",
        )
        return
    try:
        job_id = uuid.uuid4()
        print("Uuid:", job_id)
        process = Popen(
            [
                sys.executable,
                "main.py",
                "--uniprot-entry",
                uniprot_entry,
                "--save",
                "--output-folder",
                str(job_id),
            ],
            text=True,
        )
        ui.notify("Job received!")
        with ui.card():
            job_id_text = ui.label(f"Job ID: {job_id}").classes("text-blue-500")
            spinner = ui.spinner(size="lg")
            with ui.row() as myrow:
                pass

        def monitor_process():

            job_output_path = OUTPUT_FOLDER_PATH / str(job_id)
            job_output_path.mkdir(parents=True, exist_ok=True)
            config_man.save(output_path=job_output_path)
            process.wait()
            print("process complete")
            # TODO: Due to running out of time, reusing ConfigManager but it should probably be its own class as result.json is a lot different looking.
            job_result = ConfigManager(config_path=job_output_path / RESULT_NAME)
            print(job_result.conf)
            jalview_url = job_result.conf.jalview_url
            model_path = job_result.conf.model_path
            sss_uniprot_url = job_result.conf.sss_uniprot_url
            print("SSS", sss_uniprot_url)
            spinner.delete()

            with myrow:
                ui.link(
                    text=f"UNIPROT Blast Results: {sss_uniprot_url}",
                    target=sss_uniprot_url,
                )
                ui.button(
                    text="Open Jalview",
                    on_click=lambda: open_jalview(jalview_url, str(job_id)),
                )
                ui.button(
                    text="Open ChimeraX",
                    on_click=lambda: open_chimerax(model_path, str(job_id)),
                )

        threading.Thread(target=monitor_process, daemon=True).start()

    except Exception as e:
        ui.notify(f"Error: {e}")


def save_settings() -> None:

    print("Save Settings")
    config_man.save()
    ui.notification(message="Settings Saved", type="info")


def settings_handler(e: ValueChangeEventArguments, key_str: str) -> None:
    """
    Takes key_str and It basically converts "chimerax_exe_path" into conf.chimerax_exe_path
    TODO:Figure out a way to do this better
    """

    conf = config_man.conf
    keys = key_str.split(".")
    for key in keys[:-1]:
        if key not in conf:
            raise Exception(
                f"ERROR in setting_handler. onChange for {key_str} does not match config.json"
            )
        conf = conf[key]
    # Set the value at the final key
    conf[keys[-1]] = e.value


# TODO: Fix so that Reset Settings updates UI
def reset_settings_handler():
    config_man.reset()
    ui.notification(
        message="Settings Reset. The UI has not been updated but settings value has been reset",
        type="info",
    )
    print(config_man.conf.chimerax.exe_path)


def find_exe_path():
    if autodetect_os_setting(config_man.conf):
        chimerax_exe_input.set_value(config_man.conf.chimerax.exe_path)
        jalview_exe_input.set_value(config_man.conf.jalview.exe_path)
        ui.notification(
            message=f"ChimeraX exe path: {config_man.conf.chimerax.exe_path}",
            type="positive",
        )
        ui.notification(
            message=f"Jalview exe path: {config_man.conf.jalview.exe_path}",
            type="positive",
        )
    else:
        ui.notification(
            message=f"Failed to Detect exe Path",
            type="negative",
        )


with ui.card():
    ui.markdown("## Settings")
    # TODO: Combine Choose file and the path into a better icon pattern https://nicegui.io/documentation/input
    with ui.row():
        chimerax_exe_input = ui.input(
            label="ChimeraX exe path",
            value=config_man.conf.chimerax.exe_path,
            on_change=lambda e: settings_handler(e, "chimerax.exe_path"),
        ).classes("w-80")
        ui.button(
            "Choose file", on_click=lambda: pick_file(chimerax_exe_input), icon="folder"
        )
    with ui.row():
        jalview_exe_input = ui.input(
            label="Jalview exe path",
            value=config_man.conf.jalview.exe_path,
            on_change=lambda e: settings_handler(e, "jalview.exe_path"),
        ).classes("w-80")
        ui.button(
            "Choose file", on_click=lambda: pick_file(jalview_exe_input), icon="folder"
        )
    ui.button(
        "Try to automatically find exe_path",
        on_click=find_exe_path,
        icon="search",
    )
    ui.button("Save Settings", on_click=lambda: save_settings(), icon="save")
    ui.button(
        "Reset Settings",
        on_click=reset_settings_handler,
        icon="restart_alt",
    )
ui.separator()
ui.markdown("## Type of program")
job_type_arr = [
    "Method 1: Yeast across all species",
    "Method 2: NOT IMPLEMENTED",
    "Method 3: NOT IMPLEMENTED",
]
with ui.card():
    method_options = ui.toggle(
        job_type_arr,
        value=job_type_arr[0],
    )
    uniprot_entry = ui.input(
        label="UNIPROT Entry",
        placeholder="Ex. P54199 for MPS1 YEAST",
        # on_change=lambda e:,
    ).classes("w-80")
    ui.markdown("### Method Settings")
    # TODO: Add validation
    ui.number(
        label="Minimum Target Match (%)",
        value=config_man.conf.sequence_similarly_search.parse.target_match,
        on_change=lambda e: settings_handler(
            e, "sequence_similarly_search.parse.target_match"
        ),
    )
    ui.number(
        label="Max number of protein",
        value=config_man.conf.sequence_similarly_search.parse.max_entries,
        on_change=lambda e: settings_handler(
            e, "sequence_similarly_search.parse.max_entries"
        ),
    )
    ui.button(text="Run", on_click=lambda: run_main(uniprot_entry.value))

# @ui.page("/")
# def index():


ui.run(dark=True, reload=False, port=native.find_open_port())
