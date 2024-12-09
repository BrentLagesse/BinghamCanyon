import json
from pathlib import Path
import sys

from classes import (
    NCIBlASTPlus,
    JobDispatcherRESTAPI,
    ClustalOmega,
    AlphaFoldRESTAPI,
    Jalview,
    Chimerax,
    SSSTest,
    DBFetch,
    NCIBlastPlusParseTest,
)
from utils.config import ConfigManager


PRO_MODEL = AlphaFoldRESTAPI()
config_manager = ConfigManager(Path("config.json"))
# Config.reset(conf)
chimerax = Chimerax(exe_path=config_manager.conf.chimerax.exe_path, is_window=True)
jalview = Jalview(
    exe_path=config_manager.conf.jalview.exe_path,
    is_window=True,
)

seq_db = DBFetch(
    is_individually_retrieved=config_manager.conf.sequence_database.db_fetch.is_individually_retrieved
)
# SSS = NCIBlASTPlus(
# SSS = NCIBlASTPlus(
#     job_dispatcher=JobDispatcherRESTAPI("ncbiblast"),
#     sequence_database=seq_db,
#     check_delay=conf.sequence_similarly_search.nci_blast_plus.check_delay,
# )
# SSS = SSSTest(sequence_database=seq_db)
MSA = ClustalOmega(
    job_dispatcher=JobDispatcherRESTAPI("clustalo"),
    check_delay=config_manager.conf.multiple_sequence_alignment.clustal_omega.check_delay,
)

INPUT_MODE = False
output_folder_path = Path(config_manager.conf.output_folder)


def main():
    # Iterate through all files in the folder and delete them
    for file in output_folder_path.iterdir():
        if file.is_file():
            file.unlink()  # Delete the file

    UNIPROT_ENTRY = "P54199"
    if INPUT_MODE:
        print("Enter UNIPROT_ENTRY: Ex. P54199")
        UNIPROT_ENTRY = input()
    # Gets model and protein from alphafold
    seq, model_path = PRO_MODEL.run(
        unique_id=UNIPROT_ENTRY, output_folder=output_folder_path
    )
    # Finds similar dna sequeunce and returns FASTA format of similar proteins
    sss_result_path, sss_job_id = SSS.run(seq, settings="NOT YET IMPLEMENTED")

    # write job ID to err so it can be used in display
    sys.stderr.write(f"JOB ID: {sss_job_id}")

    sss_fasta_path = SSS.parse(
        sss_result_path=sss_result_path,
        target_match=config_manager.conf.sequence_similarly_search.parse.target_match,
        max_entries=config_manager.conf.sequence_similarly_search.parse.max_entries,
    )
    # aligns DNA and returns jalview url
    aln_path, jalview_url = MSA.run(sss_fasta_path, settings="NOT YET IMPLEMENTED")
    print(jalview_url)

    # write urls to stderr so they can be used in display
    sys.stderr.write(f"MODEL PATH: {model_path}")
    sys.stderr.write(f"JALVIEW URL: {jalview_url}")

    jalview.open(jalview_url)
    chimerax.open(model_path)


if __name__ == "__main__":
    main()
