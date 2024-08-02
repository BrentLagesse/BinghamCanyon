from typing import Protocol
from classes.job_dispatcher import JobDispatcher
import time
from pathlib import Path
import json
from functools import reduce


class SequenceSimilarlySearch(Protocol):
    """"Given DNA Sequeunce, finds similar DNA sequeunce from database"""
    def run(self, seq :str, settings : any) -> str:
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
    def run(self, seq :str, settings : any) -> str: 
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
        'sequence': (None, seq),
        'database': (None, 'uniprotkb_refprotswissprot'),
        }
        
        job_id = self.job_dispatcher.submit_job(parameter = parameter)
        print(job_id)
        time_waited = 0
        # loops until job is finished ETA: 5 minutes
        while not self.job_dispatcher.check_if_job_is_done(job_id = job_id):
            print(f'Checking if done... {time_waited}')
            time.sleep(self.check_delay)
            time_waited += self.check_delay
            if time_waited >= 10*60:
                raise Exception("NCIBLASTPLUS took too long")
            
        data = self.job_dispatcher.result(job_id=job_id, result_type="json")
        jsonpath = Path('data' + ".json")
        jsonpath.write_text(json.dumps(data, indent =2))
        # every 10th protein, up to first 20
        fasta_format = reduce( lambda acc, d: acc + f">{d['hit_def']}\n{d['hit_hsps'][0]['hsp_qseq']}\n" , data[:200:10] ,"")
        return fasta_format

class SSSTest(SequenceSimilarlySearch):
    def run(self, seq :str, settings : any) -> str:
        data = ''
        with open('data.json', 'r') as file:
            data = json.load(file)['hits']
        fasta_format = reduce( lambda acc, d: acc + f">{d['hit_def']}\n{d['hit_hsps'][0]['hsp_qseq']}\n" , data[:200:10] ,"")
        return fasta_format