# from chimerax.core.session import Session
# from chimerax.core.commands import run
from chimerax.core.commands import run

from pathlib import Path

cwd = Path.cwd()
print(cwd)
# from pathlib import Path
# The double quotes needs to be there incase the user cwd has a space like "C:\\Coding Projects"
# TODO: Figure out how to pass uuid of the job because you cannot simply pass it here
run(session, f'open "{cwd}\\output\\aligned_sequence.aln"')

# https://www.cgl.ucsf.edu/chimerax/docs/user/commands/open.html
run(session, "sequence associate /A")
run(session, "color byattribute seq_conservation palette blue:white:red range -1.5,1.5")
# run(main)
