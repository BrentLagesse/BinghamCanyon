import requests
from typing import Protocol
class JobDispatcher(Protocol):
    # static variable
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain',
    }
    # instance variable
    tool_name: str
    def __init__(self, tool_name: str) -> None:
        ...
    def parameters(self) -> str:
        """Returns available parameters"""
    def parameters_details(self, parameter: str) -> str:
        """Returns parameter details given parameter"""
    def submit_job(self, parameter: str) -> str:
        """Returns Job URL"""
    def status(self, job_id: str) -> str:
        """"Returns status from job id"""
    def result_types(self, job_id: str) -> str:
        """"Returns result types"""
    def result(self, job_id: str, result_type: str) -> any:
        """"Returns result"""
    def check_if_job_is_done(self, job_id :str):
        """Returns true when job is complete""" 
# REST API documentation: https://www.ebi.ac.uk/jdispatcher/docs/webservices/#/Result
class JobDispatcherRESTAPI(JobDispatcher):
    def __init__(self, tool_name):
        self.tool_name = tool_name

    def parameters(self) -> str:
        response = requests.get(f'https://www.ebi.ac.uk/Tools/services/rest/{self.tool_name}/parameters')
        return response.text
    def parameters_details(self, parameter :str) -> str:
        response = requests.get(f'https://www.ebi.ac.uk/Tools/services/rest/{self.tool_name}/parameters/{parameter}')
        return response.text
    
    
    def submit_job(self, parameter :str) -> str:
        # example of header and parameter

        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'Accept': 'text/plain',
        # }
        # parameter = f'email=test%40gmail.com&title=test&guidetreeout=true&addformats=false&dismatout=false&dealign=false&mbed=true&mbediteration=true&iterations=0&gtiterations=-1&hmmiterations=-1&outfmt=clustal_num&order=aligned&stype=protein&sequence={sample_seq}'
        # print(parameter
        # )
        # response = requests.post('https://www.ebi.ac.uk/Tools/services/rest/clustalo/run',  data = parameter)
        response = requests.post(f'https://www.ebi.ac.uk/Tools/services/rest/{self.tool_name}/run', data=parameter)
        return response.text
    def status(self, job_id :str) -> str:
        response = requests.get(f'https://www.ebi.ac.uk/Tools/services/rest/{self.tool_name}/status/{job_id}')
        return response.text
    def result_types(self, job_id :str) -> str:
        response = requests.get(f'https://www.ebi.ac.uk/Tools/services/rest/{self.tool_name}/resulttypes/{job_id}')
        return response.text
    def result(self, job_id :str, result_type :str) -> any:
        # Example of result_type:  aln-clustal_num
        response = requests.get(f'https://www.ebi.ac.uk/Tools/services/rest/{self.tool_name}/result/{job_id}/{result_type}')
        return response.json()
    
    def check_if_job_is_done(self, job_id :str): 
        status = self.status(job_id)
        print(status)
        return status == 'FINISHED'