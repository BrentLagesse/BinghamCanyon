from pathlib import Path
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
from argparse import ArgumentParser
from utils.save_job_result import save_job_result
from datetime import datetime
from utils.delete_directory import delete_directory
from constants import OUTPUT_FOLDER_PATH

PRO_MODEL = AlphaFoldRESTAPI()

# if config.json doesn't exist, takes default and creates it
if not Path("config.json").exists():
    source_file = Path("config-default.json")
    destination_file = Path("config.json")
    with source_file.open("rb") as src, destination_file.open("wb") as dst:
        dst.write(src.read())
    raise Exception(
        "NOT YET IMPLEMENTED: PLEASE either use UI to get EXE path automatically or manually edit config.json and fill out the exe path of jalview and chimerax and rerun"
    )

config_manager = ConfigManager(Path("config.json"))
chimerax = Chimerax(exe_path=config_manager.conf.chimerax.exe_path, is_window=True)
jalview = Jalview(
    exe_path=config_manager.conf.jalview.exe_path,
    is_window=True,
)

seq_db = DBFetch(
    is_individually_retrieved=config_manager.conf.sequence_database.db_fetch.is_individually_retrieved
)
# You can comment SSS and replace with another one so you don't have to wait 5 minutes
SSS = NCIBlASTPlus(
    job_dispatcher=JobDispatcherRESTAPI("ncbiblast"),
    sequence_database=seq_db,
    check_delay=config_manager.conf.sequence_similarly_search.nci_blast_plus.check_delay,
)
# SSS = NCIBlastPlusParseTest(
#     job_dispatcher=JobDispatcherRESTAPI("ncbiblast"),
#     sequence_database=seq_db,
#     check_delay=config_manager.conf.sequence_similarly_search.nci_blast_plus.check_delay,
# )
# SSS = SSSTest(sequence_database=seq_db)
MSA = ClustalOmega(
    job_dispatcher=JobDispatcherRESTAPI("clustalo"),
    check_delay=config_manager.conf.multiple_sequence_alignment.clustal_omega.check_delay,
)

INPUT_MODE = False
output_folder_path = Path(config_manager.conf.output_folder)
OPEN_PROGRAMS = True
DELETE_LAST_OUTPUT = False


def main(UNIPROT_ENTRY: str = "P54199"):
    if DELETE_LAST_OUTPUT:
        delete_directory(OUTPUT_FOLDER_PATH)
    # TODO: exist_ok should be false if --output-folder is specified as that means there a clash in uuid which shouldn't happen
    output_folder_path.mkdir(parents=True, exist_ok=True)
    start_time = datetime.now()
    if INPUT_MODE:
        print("Enter UNIPROT_ENTRY: Ex. P54199")
        UNIPROT_ENTRY = input()
    # Gets model and protein from alphafold
    seq, model_path = PRO_MODEL.run(
        unique_id=UNIPROT_ENTRY, output_folder=output_folder_path
    )
    # Finds similar dna sequeunce and returns FASTA format of similar proteins
    sss_result_path, sss_uniprot_url = SSS.run(seq, settings="NOT YET IMPLEMENTED")

    sss_fasta_path = SSS.parse(
        sss_result_path=sss_result_path,
        target_match=config_manager.conf.sequence_similarly_search.parse.target_match,
        max_entries=config_manager.conf.sequence_similarly_search.parse.max_entries,
    )
    # aligns DNA and returns jalview url
    aln_path, jalview_url = MSA.run(sss_fasta_path, settings="NOT YET IMPLEMENTED")
    print(jalview_url)

    save_job_result(
        method=1,
        model_path=model_path,
        output_path=output_folder_path,
        sss_uniprot_url=sss_uniprot_url,
        protein_uniprot_entry=UNIPROT_ENTRY,
        jalview_url=jalview_url,
        start_time=start_time,
        end_time=datetime.now(),
    )
    if OPEN_PROGRAMS:
        jalview.open(jalview_url)
        chimerax.open(model_path)


if __name__ == "__main__":
    # Handles arguments passed through the command line
    arg_parser = ArgumentParser(description="Parse to set variables, etc")
    arg_parser.add_argument(
        "-u",
        "--uniprot-entry",
        type=str,
        help="Uniprot Entry to run method with",
    )
    arg_parser.add_argument(
        "-n",
        "--no-open",
        action="store_true",
        help="Doesn't open Chimerax and Jalview",
    )
    # TODO: Figure out better name for this argument
    arg_parser.add_argument(
        "-s",
        "--save",
        action="store_true",
        help="does not delete anything in output folder",
    )
    arg_parser.add_argument(
        "-o",
        "--output-folder",
        type=str,
        help="specify output folder name to be in output/",
    )
    args = arg_parser.parse_args()

    OPEN_PROGRAMS = not args.no_open
    DELETE_LAST_OUTPUT = not args.save
    if args.output_folder:
        output_folder_path = output_folder_path / args.output_folder
    if args.uniprot_entry:
        main(args.uniprot_entry)
    else:
        main()
