import json
from pathlib import Path

from classes import NCIBlASTPlus, JobDispatcherRESTAPI, ClustalOmega, AlphaFoldRESTAPI, Jalview, Chimerax, SSSTest
# from multiprocessing import Process
import subprocess
# from threading import Thread

# from classes.job_dispatcher import JobDispatcherRESTAPI
# from classes.sequence_similarly_search import NCIBlASTPlus
# from classes.multiple_sequence_alignment import ClustalOmega
PRO_MODEL = AlphaFoldRESTAPI()

chimerax = Chimerax("C:\\Program Files\\ChimeraX 1.8\\bin\chimerax.exe", True)
# SSS = NCIBlASTPlus(job_dispatcher= JobDispatcherRESTAPI('ncbiblast'),check_delay = 10)
SSS = SSSTest()
MSA = ClustalOmega(job_dispatcher=JobDispatcherRESTAPI('clustalo'), check_delay=5)
jalview = Jalview(exe_path='C:\\Users\\chhor\\AppData\\Local\\Jalview\\bin\\jalview.bat', is_window=True)

INPUT_MODE = False

def main() :
    UNIPROT_ENTRY = 'P54199'
    if INPUT_MODE : 
        print("Enter UNIPROT_ENTRY: Ex. P54199")
        UNIPROT_ENTRY= input() 
    # Gets model and protein from alphafold 
    seq, model_path = PRO_MODEL.run(UNIPROT_ENTRY , Path("output"))
    # Finds similar dna sequeunce and returns FASTA format of similar proteins
    SSS_result = SSS.run(seq, settings= "NOT YET IMPLEMENTED")
    # aligns DNA and returns jalview url
    jalview_url = MSA.run(SSS_result, settings = "NOT YET IMPLEMENTED")
    print(jalview_url)
    
    jalview.open(jalview_url)
    chimerax.open(model_path)
    
    
if __name__ == '__main__':
    main()