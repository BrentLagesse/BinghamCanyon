from pathlib import Path
import sys
from chimerax.core.commands import run

# Usage:
# ChimeraX --script automate_conservation.py <model_path> [alignment_path]

def safe(cmd: str):
    try:
        run(session, cmd)
    except Exception as e:
        # Keep script running even if a command doesn't apply (e.g., model IDs differ)
        print(f"[ChimeraX script] Command failed: {cmd}\n  -> {e}")

model_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else None
aln_path = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else None

if model_path and model_path.exists():
    safe(f'open "{model_path.as_posix()}"')
else:
    print("[ChimeraX script] No valid model path provided; exiting.")
    raise SystemExit(1)

# OPTIONAL: If multiple ChimeraX models get created and you only want the best one visible,
# uncomment ONE of these (it depends how the CIF loads on your machine).
# safe("hide #2-9999")   # hides everything except #1
# safe("show #1")        # show #1 (if present)

if aln_path and aln_path.exists():
    safe(f'open "{aln_path.as_posix()}"')

    # Best-effort automatic association:
    # This often works if the chain is A and the query sequence is the top sequence in the alignment.
    # If your structure chain is not A, change /A below accordingly.
    safe("sequence associate /A")

    # Now color by conservation exactly as your professor said
    safe("color byattr seq_conservation palette blue:white:red range -2,2")
else:
    print("[ChimeraX script] No alignment file provided; opened model only.")