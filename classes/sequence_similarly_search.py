from typing import Protocol
from classes.job_dispatcher import JobDispatcher
import time

class SequenceSimilarlySearch(Protocol):
    """"Given DNA Sequeunce, finds similar DNA sequeunce from database"""
    def run(self, seq :str, settings : any) :
        """Runs and returns Similarly Search Data"""
        
class NCIBlASTPlus(SequenceSimilarlySearch):
    job_dispatcher : JobDispatcher
    check_delay : int
    # ensures jobDispatcher is readonly
    @property
    def value(self):
        return self._jobDispatcher
    
    def __init__(self, job_dispatcher : JobDispatcher, check_delay: int):
        self.job_dispatcher = job_dispatcher
        self.check_delay = check_delay
    def run(self, seq :str, settings : any) : 
        # To Do: add settings customization
        parameter = {
        'email': (None, 'test@gmail.com'),
        'program': (None, 'blastp'),
        'matrix': (None, 'BLOSUM62'),
        'alignments': (None, '250'),
        'scores': (None, '250'),
        'exp': (None, '10'),
        'filter': (None, 'F'),
        'gapalign': (None, 'true'),
        'compstats': (None, 'F'),
        'align': (None, '0'),
        'stype': (None, 'protein'),
        'sequence': (None, f'>{seq}'),
        'database': (None, 'uniprotkb_refprotswissprot'),
        }
        
        job_id = self.job_dispatcher.submit_job(parameter = parameter)
        print(job_id)
        i = 0
        # loops until job is finished ETA: 5 minutes
        while not self.job_dispatcher.check_if_job_is_done(job_id = job_id):
            print(f'Checking if done... {i}')
            time.sleep(self.check_delay)
            i +=1
        return self.job_dispatcher.result(job_id=job_id, result_type="json")
    
    