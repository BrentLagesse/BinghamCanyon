import requests
import subprocess

# imports to fix MutableMapping working in old python
import collections
from collections import abc
collections.MutableMapping = abc.MutableMapping

from intermine.webservice import Service
from intermine import registry

# build queries
# https://www.alliancegenome.org/alliancemine/customQuery.do
print(registry.getData("AllianceMine"))

def number_to_alphabet(index):
    # Ensure the index is within the range 0-25
    if 0 <= index < 26:
        # Convert index to corresponding uppercase alphabet
        return chr(index + ord('A'))
    else:
        raise ValueError("Index out of range. Must be between 0 and 25.")
    
#Step 7-9
def get_yeast_genome_protein_seq(systematic_name_arr : list[str]) -> str:
    
    if(len(systematic_name_arr) == 0):
        print("get_yeast_genome_protein_seq input was null")
        return
    # The following two lines will be needed in every python script:
    # from intermine.webservice import Service
    service = Service("https://www.alliancegenome.org/alliancemine/")
    # service = Service("http://agr.stage.alliancemine.tomcat.server:8080/alliancemine/service")

    # some reason standard name cannot be used, so using systematic name instead
    # systematic_name = "YIL170W"

    # Get a new query on the class (table) you will be querying:
    query = service.new_query("Protein")

    # The view specifies the output columns
    query.add_view("sequence.residues", "symbol")

    # Uncomment and edit the line below (the default) to select a custom sort order:
    # query.add_sort_order("Protein.sequence.residues", "ASC")

    # You can edit the constraint values below
    logic_statement =''
    for i, name in enumerate(systematic_name_arr) :
        letter = number_to_alphabet(i)
        query.add_constraint("secondaryIdentifier", "=", name, code=letter)
        if i != len(systematic_name_arr) -1:
            logic_statement += f'{letter} or '
    last_letter = number_to_alphabet(len(systematic_name_arr)-1)
    logic_statement += last_letter
    print(logic_statement)
    query.set_logic(logic_statement)

    result = query.rows()
    if len(result) == 0:
        print(f'ERROR no proteins found')
        return
    if len(result) != len(systematic_name_arr):
        print(f'ERROR protein found does not match up : {len(systematic_name_arr)} != {len(result)}')
        return
    
    clustal_omega_seq = ''
    for row in result:
        protein_seq = row["sequence.residues"] 
        standard_name = row["symbol"]
        print(standard_name)
        clustal_omega_header = f'>{standard_name}'
        clustal_omega_seq += f'{clustal_omega_header}\n{protein_seq}\n'
    return clustal_omega_seq


yeast_genome_seq = get_yeast_genome_protein_seq(["YIL170W","YIL171W"])
print(yeast_genome_seq)
sample_seq = yeast_genome_seq

# 2 Protein seq from yeastgenome
# sample_seq= """>DOG2 YHR043C SGDID:S000001085
# MPQFSVDLCLFDLDGTIVSTTTAAESAWKKLCRQHGVDPVELFKHSHGARSQEMMKKFFP
# KLDNTDNKGVLALEKDMADNYLDTVSLIPGAENLLLSLDVDTETQKKLPERKWAIVTSGS
# PYLAFSWFETILKNVGKPKVFITGFDVKNGKPDPEGYSRARDLLRQDLQLTGKQDLKYVV
# FEDAPVGIKAGKAMGAITVGITSSYDKSVLFDAGADYVVCDLTQVSVVKNNENGIVIQVN
# NPLTRD*
# >HXT12 YIL170W SGDID:S000001432
# MGLIVSIFNIGCAIGGIVLSKVGDIYGRRIGLITVTAIYVVGILIQITSINKWYQYFIGR
# IISGIGVGGIAVLSPMLISEVAPKHIRGTLVQLYQLMGTMGIFLGYCTNYGTKNYHNATQ
# WRVGLGLCFAWATFMVSGMMFVPESPRYLIEVGKDEEAKHSLSKSNKVSVDDPALLAEYD
# TIKAGIEIEKLAGNASWSELLSTKTKVFQRVLMGVIIQSLQQLTGDNYFFYYGTTIFKSV
# GLKDSFQTSIIIGVVNFFSSFIAVYTIERFGRRTCLLWGAASMLCCFAVFASVGVTKLWP
# QGSSHQDITSQGAGNCMIVFTMFFIFSFATTWAGGCFVIVSETFPLRAKSRGMAIATAAN
# WMWGFLISFFTPFITGAINFYYGYVFLGCLVFAYFYVFFFVPETKGLTLEEVNTMWLEGV
# PAWKSASWVPPERRTADYDADAIDHDNRPIYKRFFSS*
# """

# step 10 & step 11
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/plain',
}

data = f'email=test%40gmail.com&title=test&guidetreeout=true&addformats=false&dismatout=false&dealign=false&mbed=true&mbediteration=true&iterations=0&gtiterations=-1&hmmiterations=-1&outfmt=clustal_num&order=aligned&stype=protein&sequence={sample_seq}'

response = requests.post('https://www.ebi.ac.uk/Tools/services/rest/clustalo/run', headers=headers, data=data)

jobId = response.text

print("jobId:", jobId)

jalview_url = 'https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/'+ jobId+ '/aln-clustal_num'
print("jalview url: ",jalview_url)

# # step 12
# jalview_exe_path = 'C:\\Users\\chhor\\AppData\\Local\\Jalview\\bin\\jalview.bat'
# subprocess.run(['jalview_exe_path', "https://www.ebi.ac.uk/Tools/services/rest/clustalo/result/clustalo-R20240709-165430-0694-644924-p1m/aln-clustal_num"], shell = True)

