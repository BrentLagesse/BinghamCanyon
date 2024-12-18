import sys

sys.path.append("C:\\Program Files\\ChimeraX 1.8\\bin\chimerax.exe")

# Now you can import modules from 'mypackage'
import chimerax.core.commands


# ChimeraX script to automate the conservation coloring process
def main(session):
    # Step 4: Open the .cif files
    cif_files = [
        "/path/to/file1.cif",
        "/path/to/file2.cif",
        "/path/to/file3.cif",
        "/path/to/file4.cif",
        "/path/to/file5.cif",
    ]
    for cif_file in cif_files:
        session.open_command.open_data(cif_file)

    # Step 5: Overlay using Matchmaker
    session.run_command("mm #")  # Match all models using default settings

    # Step 6: Open the Jalview alignment
    jalview_alignment = "/path/to/alignment.jalview"
    session.open_command.open_data(jalview_alignment)

    # Step 7: Associate the alignment with the first model
    session.run_command("structure association #1")  # Assuming #1 is the first model

    # Step 8: Color by sequence conservation
    session.run_command(
        "color byattr seq_conservation palette blue:white:red range -1.5,1.5"
    )

    # Step 13: Uncheck models for easier viewing (only show the first model)
    session.run_command("modeldisplay #1")
    session.run_command("modeldisplay #2 off")
    session.run_command("modeldisplay #3 off")
    session.run_command("modeldisplay #4 off")
    session.run_command("modeldisplay #5 off")


# Required to execute as a ChimeraX script
from chimerax.core.commands import run

run(main)
