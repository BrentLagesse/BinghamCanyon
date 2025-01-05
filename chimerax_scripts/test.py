# from chimerax.core.session import Session
# from chimerax.atomic import structure
from chimerax.core.commands import run


run(session, "windowsize 10 10")

# https://www.cgl.ucsf.edu/chimerax/docs/user/commands/open.html
run(session, " open ~\\Downloads\\test_clustal.aln")
# run(
#     session,
#     ' open "C:\Coding Projects\BinghamCanyon\BinghamCanyon\test\sss_fasta_format.fasta"',
# )
# run(session, 'open "C:\\Users\\chhor\\Downloads\\test\\clustal.aln"')
# run(session, 'open "/test/clustal.aln"')
run(session, "sequence associate /A")
run(session, "color byattribute seq_conservation palette blue:white:red range -1.5,1.5")
# def main(session):
#     print("FInished")


# # Start a new session
# session = Session("test")

# # Load a PDB file (replace with your PDB file path)
# # session.open_command.open_data("/path/to/your_file.pdb")

# # Run a visualization command
# session.logger.status("Displaying molecule...")
# session.run_command("show")
