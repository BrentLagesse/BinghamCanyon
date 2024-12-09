from typing import Protocol
from classes.job_dispatcher import JobDispatcher
import time
from pathlib import Path
import requests
import json


class MultipleSequenceAlignment(Protocol):
    """ "Given DNA sequence, finds similar DNA sequence from database"""

    def run(self, seq: str, settings: any) -> tuple[Path, str]:
        """Runs and returns url for JalView to open. Also creates .aln file that will be used in UCSFX"""


class ClustalOmega(MultipleSequenceAlignment):
    """
    Documentation for REST API used: https://www.ebi.ac.uk/jdispatcher/docs/webservices/#clients
    """

    check_delay: int
    job_dispatcher: JobDispatcher

    def __init__(self, job_dispatcher: JobDispatcher, check_delay):
        self.job_dispatcher = job_dispatcher
        self.check_delay = check_delay

    def run(self, seq_path: Path, settings: any) -> tuple[Path, str]:
        # print(f"PROGRESS: multiple_sequence_alignment (ClustalOmega): job_id")
        seq = seq_path.read_text(encoding="utf-8")
        parameter = {
            "email": (None, "test@gmail.com"),
            "sequence": (None, seq),
        }
        job_id = self.job_dispatcher.submit_job(parameter)
        print(job_id)
        time_waited = 0
        while not self.job_dispatcher.check_if_job_is_done(job_id=job_id):
            print(f"Checking if ClustalOmega is done... {time_waited}")
            time.sleep(self.check_delay)
            time_waited += self.check_delay
            if time_waited >= 1 * 60:
                raise Exception("ClustalOmega took too long")
        result_url = f"https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{job_id}/aln-clustal_num"
        response = requests.get(result_url)
        aligned_seq = response.text
        aln_path = Path("output/aligned_sequence" + ".aln")
        aln_path.write_text(aligned_seq)
        return aln_path, result_url
