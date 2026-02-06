from pathlib import Path
import sys

from chimerax.core.commands import run

# This script is launched by chimerax.py like:
#   ChimeraX --script chimerax_scripts/automate_conservation.py <model_path>
#
# Any arguments after the script path are available in sys.argv here.
# sys.argv[0] is this script file.
model_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else None

if model_path and model_path.exists():
    run(session, f'open "{model_path.as_posix()}"')
else:
    # If no model is provided, do nothing (ChimeraX will still open).
    pass

# If you later want to pass an alignment file too, you can add it as argv[2] and uncomment below:
# aln_path = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else None
# if aln_path and aln_path.exists():
#     run(session, f'open "{aln_path.as_posix()}"')
#     run(session, "sequence associate /A")
#     run(session, "color byattribute seq_conservation palette blue:white:red range -1.5,1.5")