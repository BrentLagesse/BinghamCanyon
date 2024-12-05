import json
from pathlib import Path

from classes import (
    NCIBlASTPlus,
    JobDispatcherRESTAPI,
    ClustalOmega,
    AlphaFoldRESTAPI,
    Jalview,
    Chimerax,
    SSSParseTest,
    DBFetch,
    NCIBlastPlusParseTest,
)

# from classes.job_dispatcher import JobDispatcherRESTAPI
# from classes.sequence_similarly_search import NCIBlASTPlus
# from classes.multiple_sequence_alignment import ClustalOmega


PRO_MODEL = AlphaFoldRESTAPI()

chimerax = Chimerax("C:\\Program Files\\ChimeraX 1.8\\bin\chimerax.exe", True)

DB_fetch = DBFetch(is_individually_retrieved=True)
SSS = NCIBlASTPlus(
    job_dispatcher=JobDispatcherRESTAPI("ncbiblast"),
    sequence_database=DB_fetch,
    check_delay=10,
)
# SSS = NCIBlastPlusParseTest(
#     job_dispatcher=JobDispatcherRESTAPI("ncbiblast"),
#     sequence_database=DB_fetch,
#     check_delay=10,
# )
# SSS = SSSTest(sequence_database=DB_fetch)
MSA = ClustalOmega(job_dispatcher=JobDispatcherRESTAPI("clustalo"), check_delay=5)
jalview = Jalview(
    exe_path="C:\\Users\\chhor\\AppData\\Local\\Jalview\\bin\\jalview.bat",
    is_window=True,
)

INPUT_MODE = False
output_folder_path = Path("output")


def main():
    # Iterate through all files in the folder and delete them
    for file in output_folder_path.iterdir():
        if file.is_file():  # Check if it is a file
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
    sss_fasta_path = SSS.parse(
        sss_result_path=sss_result_path,
        target_match=50,
        max_entries=20,
    )
    # aligns DNA and returns jalview url
    jalview_url = MSA.run(sss_fasta_path, settings="NOT YET IMPLEMENTED")
    print(jalview_url)
    jalview.open(jalview_url)
    chimerax.open(model_path)


if __name__ == "__main__":
    main()
