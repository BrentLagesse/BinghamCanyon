from typing import Protocol
from classes.job_dispatcher import JobDispatcher
from classes.sequence_database import SequenceDatabase
import time
from pathlib import Path
import json


class SequenceSimilarlySearch(Protocol):
    """Given DNA Sequence, finds similar DNA sequence from database"""

    def run(self, seq: str, settings: any) -> tuple[Path, str]:
        """Runs and returns Similarly DNA sequence

        Args:
            seq (str): RNA sequence
            settings (any): TODO: figure out what settings should be

        Returns:
            tuple[Path, str]: Path = path of unparsed SSS result. str = job id
        """

    def parse(self, sss_result_path: Path, target_match: int, max_entries: int) -> Path:
        """
        Parses SSS data fo for Jalview
        Args:
            target_match (int): (1-100)% that the sequence matches >= target_math
            max_entries (int): max entries
        Returns:
            str: FASTA format of resulted SSS
        """


class NCIBlASTPlus(SequenceSimilarlySearch):
    job_dispatcher: JobDispatcher
    sequence_database: SequenceDatabase
    check_delay: int

    def __init__(
        self,
        job_dispatcher: JobDispatcher,
        sequence_database: SequenceDatabase,
        check_delay: int,
    ):
        self.job_dispatcher = job_dispatcher
        self.sequence_database = sequence_database
        self.check_delay = check_delay

    def run(self, seq: str, settings: any) -> tuple[Path, str]:
        # TODO: add settings customization
        parameter = {
            "email": (None, "test@gmail.com"),
            "program": (None, "blastp"),
            "matrix": (None, "BLOSUM62"),
            "alignments": (None, "250"),
            "scores": (None, "1000"),
            "exp": (None, "10"),
            "filter": (None, "F"),
            "gapalign": (None, "true"),
            "compstats": (None, "F"),
            "align": (None, "0"),
            "stype": (None, "protein"),
            "sequence": (None, seq),
            "database": (None, "uniprotkb_refprotswissprot"),
        }
        job_id = self.job_dispatcher.submit_job(parameter=parameter)
        print(f"PROCESS: Sequence Similarly Search (Blast) on Job_ID: {job_id}")
        seconds_waited = 0
        # loops until job is finished ETA: 5 minutes
        while not self.job_dispatcher.check_if_job_is_done(job_id=job_id):
            print(f"\tIN PROGRESS: {seconds_waited} seconds")
            time.sleep(self.check_delay)
            seconds_waited += self.check_delay
            if seconds_waited >= 15 * 60:
                raise Exception("NCIBLASTPLUS took too long")
        data = self.job_dispatcher.result(job_id=job_id, result_type="json")
        sss_result_path = Path("output/sss_all_data" + ".json")
        sss_result_path.write_text(json.dumps(data, indent=2))
        # TODO: job_id returns url for bio to look at https://www.uniprot.org/blast/uniprotkb/ncbiblast-R20241124-010053-0510-42992132-p1m/overview
        uniprot_url = f"https://www.uniprot.org/blast/uniprotkb/{job_id}/overview"
        print(
            f"COMPLETE: Sequence Similarly Search (Blast) on Job_ID: {job_id} \n URL: https://www.uniprot.org/blast/uniprotkb/{job_id}/overview"
        )
        return sss_result_path, uniprot_url

    def parse(self, sss_result_path: Path, target_match: int, max_entries: int) -> Path:
        print(f"PROCESS: Parsing Sequence Similarly Search (Blast)'s data")
        if target_match <= 0 or target_match > 100:
            raise IndexError("Target match should be greater than 0 and less than 1")
        with sss_result_path.open("r") as file:
            data = json.load(file)

            def is_seq_within_target_match(hit, target_match: int):
                """
                Filters so that the sequence matches >= target_math
                """
                dna_length = hit["hit_len"]
                part_match = (
                    hit["hit_hsps"][0]["hsp_hit_to"]
                    - hit["hit_hsps"][0]["hsp_hit_from"]
                )
                # Check in case math is incorrect
                if part_match / dna_length > 1:
                    print(
                        hit["hit_hsps"][0]["hsp_query_to"],
                        hit["hit_hsps"][0]["hsp_query_from"],
                        dna_length,
                    )
                    raise IndexError(f"Somehow {hit['hit_acc']} is greater than 100%")
                return (part_match * 100 // dna_length) >= target_match

            # Grabs all useful hits into an array if_seq_within_target_march
            def optimal_diversified(target_number: int, length: int):
                """
                Finds optimal number to get target
                """
                return length // target_number

            useful_hits = [
                hit
                for hit in data["hits"]
                if is_seq_within_target_match(hit, target_match)
            ]
            sss_target_match_path = Path("output/sss_within_target_match" + ".json")
            sss_target_match_path.write_text(json.dumps(useful_hits, indent=2))
            print("useful_hits:", len(useful_hits))
            number_to_skip = optimal_diversified(max_entries, len(useful_hits))
            print("number_to_skip:", number_to_skip)
            useful_hits = useful_hits[::number_to_skip][:max_entries]
            sss_target_match_path_nth = Path(
                "output/sss_within_target_match_nth" + ".json"
            )
            sss_target_match_path_nth.write_text(json.dumps(useful_hits, indent=2))
            # TODO: Make it all in one loop instead
            uniprot_entries = (hit["hit_acc"] for hit in useful_hits)
            # convert into list because generator cannot be accessed by index
            header = list(
                (
                    f">{hit['hit_os']} {hit['hit_uni_de']} UNIPROT Entry: +  {hit['hit_acc']}"
                    for hit in useful_hits
                )
            )
            protein_sequence_arr = self.sequence_database.lookup_many(
                entry_list=uniprot_entries
            )
            fasta_format = ""
            for i, protein_sequence in enumerate(protein_sequence_arr):
                # replaced spaces because anything after spaces gets deleted
                fasta_format += (
                    header[i].replace(" ", "~") + "\n" + protein_sequence + "\n"
                )
            # TODO: gets rid of last \n
            fasta_path = Path("output/sss_fasta_format" + ".fasta")
            fasta_path.write_text(fasta_format)
            print(f"COMPLETE: Parsing Sequence Similarly Search (Blast)'s data")
            return fasta_path


class SSSTest(SequenceSimilarlySearch):
    sequence_database: SequenceDatabase

    def __init__(
        self,
        sequence_database: SequenceDatabase,
    ):
        self.sequence_database = sequence_database

    def run(self, seq: str, settings: any) -> tuple[Path, str]:
        return [Path("./test/sss_all_data.json"), ""]

    def parse(self, sss_result_path: Path, target_match: int, max_entries: int) -> Path:
        return Path("./test/sss_fasta_format.fasta")


class NCIBlastPlusParseTest(NCIBlASTPlus):

    def run(self, seq: str, settings: any) -> tuple[Path, str]:
        return [Path("./test/sss_all_data.json"), ""]

    # def parse(self, sss_result_path: Path, target_match: int, max_entries: int) -> Path:
