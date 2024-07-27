from typing import Protocol
from classes.job_dispatcher import JobDispatcher
from pathlib import Path
import requests
import os
class ProteinModel(Protocol):
    """"Given DNA Sequeunce, finds similar DNA sequeunce from database"""
    def run(self, unique_id :str, output_folder : Path) -> str:
        """Runs and puts all model files in output_folder and returns Protein Sequence"""
        
# https://alphafold.ebi.ac.uk/api-docs
class AlphaFoldRESTAPI(ProteinModel):
    def run(self, unique_id :str, output_folder : Path) -> str:
        headers = {
        'accept': 'application/json',
        }

        params = {
            # api key might be private unique, so not publishing it on github
            'key': os.environ.get('ALPHA_FOLD_API_KEY='),
        }

        response = requests.get(f'https://alphafold.ebi.ac.uk/api/prediction/{unique_id}', params=params, headers=headers)
        data = response.json()
        # TODO: save image
        return data[0]['uniprotSequence']
    # Example of API response
""""[
  {
    "entryId": "AF-A0A1X7R3K2-F1",
    "gene": "KASA_0N02057G",
    "sequenceChecksum": "0961DE96565FE724",
    "sequenceVersionDate": "2017-07-05",
    "uniprotAccession": "A0A1X7R3K2",ma
    "uniprotId": "A0A1X7R3K2_9SACH",
    "uniprotDescription": "Similar to Saccharomyces cerevisiae YDL028C MPS1 Dual-specificity kinase required for spindle pole body (SPB) duplication and spindle checkpoint function",
    "taxId": 1789683,
    "organismScientificName": "Kazachstania saulgeensis",
    "uniprotStart": 1,
    "uniprotEnd": 749,
    "uniprotSequence": "MSKYKHHSRSRIQGDGDGTNLPIRSIDNNSDYGEDEDNIGPPKLSNFGSALLARGNDTGRSNFLTRLQMAETLTNPVEPHSRSQTIYSQIQDSPQSSLFATNHNNNNVNVNNRPLSMTTVHDNNGNNDEDISKHSEKFSPSSKLRSMQQHMKDELTSRYTERRINRLLLSSDRMSKLGPAKRTSSLQSIDLNDQFASNNINLQNNGSNLTTKSLSGTISTSRPILSPSNTDAVIPSAPLNDYSNIDFGDLNPLQYLKKHDLPSSELPHISKIYFEKRKEEIRRTALRKHSSSKDILLNRTRYIDENSNNNSHTSIRNNSNNRRSIDIDKGSPIIIDRSEEPPNRNSIFKEQQNIDIESNVPANDFNVKNKKREALSNISLNKREPEHKKTKKVEIQEPIKTNTYRRNNIVRVNDVEYERIEMLGRGGSSKVYKVKGPGNKVYALKRVIFDEFDESSVNGFKGEIELLQKLDRKDRVVHLYDYMMDQGLLYLIMECGDFDLSQILNTRMNDPFDVSFIRYYTKEMIECIKVVHDSGIVHSDLKPANFVVVKGKLKIIDFGIANAVPDHTVNIYRDTQIGTPNYMAPEALITMNYHDIKDKSREDSNQKLPKNTWKVGKPSDIWSCGCMLYQMVYGKPPYAGFQGQNRLLAIMNPDVKISFSEKTDHGESIVPKSLLELMKQCLIRDPDKRCTVNEILQSSFLKPVVVTEFFIKDLIKNAVTFGAKQRYVSDDKIEELTNDVLNRLEEFKM",
    "modelCreatedDate": "2022-06-01",
    "latestVersion": 4,
    "allVersions": [
      3,
      4
    ],
    "isReviewed": false,
    "isReferenceProteome": true,
    "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-A0A1X7R3K2-F1-model_v4.cif",
    "bcifUrl": "https://alphafold.ebi.ac.uk/files/AF-A0A1X7R3K2-F1-model_v4.bcif",
    "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-A0A1X7R3K2-F1-model_v4.pdb",
    "paeImageUrl": "https://alphafold.ebi.ac.uk/files/AF-A0A1X7R3K2-F1-predicted_aligned_error_v4.png",
    "paeDocUrl": "https://alphafold.ebi.ac.uk/files/AF-A0A1X7R3K2-F1-predicted_aligned_error_v4.json",
    "amAnnotationsUrl": null,
    "amAnnotationsHg19Url": null,
    "amAnnotationsHg38Url": null
  }
]"""