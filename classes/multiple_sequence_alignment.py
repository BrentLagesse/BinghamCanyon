from typing import Protocol
from classes.job_dispatcher import JobDispatcher
import time
class MultipleSequenceAlignment(Protocol):
    """"Given DNA Sequeunce, finds similar DNA sequeunce from database"""
    def run(self, seq :str, settings : any) -> str :
        """Runs and returns url for JalView to open. Also creates .aln file that will be used in UCSFX"""

# https://www.ebi.ac.uk/jdispatcher/docs/webservices/#clients
class ClustalOmega(MultipleSequenceAlignment) :
    check_delay : int
    ""
    job_dispatcher : JobDispatcher
    def __init__(self, job_dispatcher : JobDispatcher, check_delay) :
        self.job_dispatcher = job_dispatcher
        self.check_delay = check_delay
    def run(self, seq :str, settings : any) -> str :
        parameter = {
        'email': (None, 'test@gmail.com'),
        'sequence': (None, seq),
        }
        job_id = self.job_dispatcher.submit_job(parameter)
        print(job_id)
        time_waited = 0
        while not self.job_dispatcher.check_if_job_is_done(job_id = job_id):
            print(f'Checking if ClustalOmega is done... {time_waited}')
            time.sleep(self.check_delay)
            time_waited += self.check_delay
            if time_waited >= 1*60:
                raise Exception("ClustalOmega took too long")
        result_url = f'https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/{job_id}/aln-clustal_num'
        return result_url