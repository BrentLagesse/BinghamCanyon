from typing import Protocol
from classes.job_dispatcher import JobDispatcher
import time

class MultipleSequenceAlignment(Protocol):
    """"Given DNA Sequeunce, finds similar DNA sequeunce from database"""
    def run(self, seq :str, settings : any) :
        """Runs and returns url for JalView to open. Also creates .aln file that will be used in UCSFX"""
        
class ClustalOmega(MultipleSequenceAlignment) :
    job_dispatcher : JobDispatcher
    def __init__(self, job_dispatcher : JobDispatcher) :
        self.job_dispatcher = job_dispatcher
    def run(self, seq :str, settings : any) :
        parameter = {
        'email': (None, 'test@gmail.com'),
        'sequence': (None, seq),
        }
        
        return self.job_dispatcher.submit_job(parameter)