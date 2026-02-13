from pathlib import Path
import threading
from subprocess import Popen, STDOUT
from typing import Optional

import requests
from nicegui import ui, native
from nicegui.events import ValueChangeEventArguments

from utils.config import ConfigManager, Config
from utils.autodetect_os_setting import autodetect_os_setting
from components.local_file_picker import local_file_picker
from constants import OUTPUT_FOLDER_PATH, RESULT_NAME, CONFIG_NAME

import sys
import uuid
from classes import Chimerax, Jalview


# -------------------------
# config bootstrapping
# -------------------------
if not Path("config.json").exists():
    source_file = Path("config-default.json")
    destination_file = Path("config.json")
    with source_file.open("rb") as src, destination_file.open("wb") as dst:
        dst.write(src.read())

config_man = ConfigManager(Path("config.json"))

ui.markdown("# **Automated Conservation Tool**")


async def pick_file(input: ui.input) -> None:
    result = await local_file_picker("~", multiple=False)
    ui.notify(f"You chose {result}")
    input.value = result


def download_alignment_to_file(jalview_url: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(jalview_url, timeout=60)
    r.raise_for_status()
    out_path.write_text(r.text)
    return out_path


def open_jalview(aln_or_url: str, job_id: str):
    job_conf_path = Path(OUTPUT_FOLDER_PATH / job_id / CONFIG_NAME)
    job_conf = Config().load_json(str(job_conf_path))
    jalview = Jalview(
        exe_path=job_conf.jalview.exe_path,
        is_window=(sys.platform == "win32"),
    )
    jalview.open(aln_or_url)


def open_chimerax(model_path: str, job_id: str, aln_path: Optional[str] = None):
    """
    Launch ChimeraX and write a detailed launch log to:
      output/<job_id>/chimerax_launch.log
    """
    job_output_path = OUTPUT_FOLDER_PATH / str(job_id)
    log_path = job_output_path / "chimerax_launch.log"

    job_conf_path = Path(OUTPUT_FOLDER_PATH / job_id / CONFIG_NAME)
    job_conf = Config().load_json(str(job_conf_path))

    exe = Path(job_conf.chimerax.exe_path).expanduser()
    script = (Path(__file__).parent / "chimerax_scripts" / "automate_conservation.py").resolve()
    model = Path(model_path).expanduser().resolve()

    aln = None
    if aln_path:
        aln = Path(aln_path).expanduser().resolve()

    # Preflight checks
    missing = []
    if not exe.exists():
        missing.append(f"ChimeraX exe not found: {exe}")
    if not script.exists():
        missing.append(f"ChimeraX script not found: {script}")
    if not model.exists():
        missing.append(f"Model file not found: {model}")
    if aln_path and (aln is None or not aln.exists()):
        missing.append(f"Alignment file not found: {aln}")

    if missing:
        msg = "Cannot launch ChimeraX:\n" + "\n".join(missing)
        print(msg)
        ui.notify(msg, type="negative")
        return

    # Build cmd (matches chimerax.py behavior)
    cmd = [str(exe), "--script", str(script), str(model)]
    if aln is not None:
        cmd.append(str(aln))

    # Write header + capture stdout/stderr to file
    job_output_path.mkdir(parents=True, exist_ok=True)
    with log_path.open("w") as f:
        f.write("ChimeraX launch\n")
        f.write(f"exe:    {exe}\n")
        f.write(f"script: {script}\n")
        f.write(f"model:  {model}\n")
        f.write(f"aln:    {aln}\n")
        f.write("cmd:\n  " + " ".join(cmd) + "\n\n")
        f.write("---- ChimeraX output ----\n")

    print("Launching ChimeraX with cmd:", cmd)
    ui.notify(f"Launching ChimeraX… (log: {log_path})", type="info")

    # Append process output to the same log file
    with log_path.open("a") as f:
        try:
            Popen(cmd, shell=False, stdout=f, stderr=STDOUT)
        except Exception as e:
            err = f"Failed to start ChimeraX: {e}"
            print(err)
            f.write("\nERROR:\n" + err + "\n")
            ui.notify(err, type="negative")


def run_main(uniprot_entry: str):
    if uniprot_entry == "":
        ui.notification(message="Uniprot entry is empty", type="negative")
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
            ui.label(f"Job ID: {job_id}").classes("text-blue-500")
            spinner = ui.spinner(size="lg")
            with ui.row() as myrow:
                pass

        def monitor_process():
            job_output_path = OUTPUT_FOLDER_PATH / str(job_id)
            job_output_path.mkdir(parents=True, exist_ok=True)

            config_man.save(output_path=job_output_path)

            process.wait()
            print("process complete")

            job_result = ConfigManager(config_path=job_output_path / RESULT_NAME)
            print(job_result.conf)

            jalview_url = job_result.conf.jalview_url
            model_path = job_result.conf.model_path
            sss_uniprot_url = job_result.conf.sss_uniprot_url
            print("SSS", sss_uniprot_url)

            aln_file_path = job_output_path / "alignment.aln"
            aln_file_str: Optional[str] = None
            try:
                download_alignment_to_file(jalview_url, aln_file_path)
                aln_file_str = str(aln_file_path)
                print(f"Saved alignment to: {aln_file_str}")
            except Exception as e:
                print(f"Failed to download alignment file: {e}")
                aln_file_str = None

            spinner.delete()

            with myrow:
                ui.link(
                    text=f"UNIPROT Blast Results: {sss_uniprot_url}",
                    target=sss_uniprot_url,
                )

                ui.button(
                    text="Open Jalview",
                    on_click=lambda: open_jalview(aln_file_str if aln_file_str else jalview_url, str(job_id)),
                )

                ui.button(
                    text="Open ChimeraX (Colored)",
                    on_click=lambda: open_chimerax(model_path, str(job_id), aln_file_str),
                )

        threading.Thread(target=monitor_process, daemon=True).start()

    except Exception as e:
        ui.notify(f"Error: {e}", type="negative")


def save_settings() -> None:
    print("Save Settings")
    config_man.save()
    ui.notification(message="Settings Saved", type="info")


def settings_handler(e: ValueChangeEventArguments, key_str: str) -> None:
    conf = config_man.conf
    keys = key_str.split(".")
    for key in keys[:-1]:
        if key not in conf:
            raise Exception(
                f"ERROR in setting_handler. onChange for {key_str} does not match config.json"
            )
        conf = conf[key]
    conf[keys[-1]] = e.value


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
        ui.notification(message="Failed to Detect exe Path", type="negative")


with ui.card():
    ui.markdown("## Settings")
    with ui.row():
        chimerax_exe_input = ui.input(
            label="ChimeraX exe path",
            value=config_man.conf.chimerax.exe_path,
            on_change=lambda e: settings_handler(e, "chimerax.exe_path"),
        ).classes("w-80")
        ui.button("Choose file", on_click=lambda: pick_file(chimerax_exe_input), icon="folder")
    with ui.row():
        jalview_exe_input = ui.input(
            label="Jalview exe path",
            value=config_man.conf.jalview.exe_path,
            on_change=lambda e: settings_handler(e, "jalview.exe_path"),
        ).classes("w-80")
        ui.button("Choose file", on_click=lambda: pick_file(jalview_exe_input), icon="folder")

    ui.button("Try to automatically find exe_path", on_click=find_exe_path, icon="search")
    ui.button("Save Settings", on_click=lambda: save_settings(), icon="save")
    ui.button("Reset Settings", on_click=reset_settings_handler, icon="restart_alt")

ui.separator()
ui.markdown("## Type of program")

job_type_arr = [
    "Method 1: Yeast across all species",
    "Method 2: NOT IMPLEMENTED",
    "Method 3: NOT IMPLEMENTED",
]

with ui.card():
    ui.toggle(job_type_arr, value=job_type_arr[0])

    uniprot_entry = ui.input(
        label="UNIPROT Entry",
        placeholder="Ex. P54199 for MPS1 YEAST",
    ).classes("w-80")

    ui.markdown("### Method Settings")

    ui.number(
        label="Minimum Target Match (%)",
        value=config_man.conf.sequence_similarly_search.parse.target_match,
        on_change=lambda e: settings_handler(e, "sequence_similarly_search.parse.target_match"),
    )

    ui.number(
        label="Max number of protein",
        value=config_man.conf.sequence_similarly_search.parse.max_entries,
        on_change=lambda e: settings_handler(e, "sequence_similarly_search.parse.max_entries"),
    )

    ui.button(text="Run", on_click=lambda: run_main(uniprot_entry.value))

ui.run(dark=True, reload=False, port=native.find_open_port())