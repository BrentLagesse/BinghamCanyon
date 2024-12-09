from typing import Protocol
from classes.job_dispatcher import JobDispatcher
from pathlib import Path
import requests
import os


class ProteinModel(Protocol):
    """ "Given DNA Sequeunce, finds similar DNA sequeunce from database"""

    def run(self, unique_id: str, output_folder: Path) -> tuple[str, Path]:
        """Runs and puts all model files in output_folder and returns Protein Sequence"""


# https://alphafold.ebi.ac.uk/api-docs
class AlphaFoldRESTAPI(ProteinModel):
    def run(self, unique_id: str, output_folder: Path) -> tuple[str, Path]:
        headers = {
            "accept": "application/json",
        }
        params = {
            # api key might be private unique, so not publishing it on github
            "key": os.environ.get("ALPHA_FOLD_API_KEY="),
        }
        # response returns a length=1 dict
        print("PROCESS: Fetching AlphaFold Model")
        response = requests.get(
            f"https://alphafold.ebi.ac.uk/api/prediction/{unique_id}",
            params=params,
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception("Protein not found")
        data = response.json()[0]
        output_folder.mkdir(parents=True, exist_ok=True)
        model_path = output_folder / "protein_model.cif"
        with open(str(model_path), "wb") as f:
            f.write(requests.get(data["cifUrl"]).content)
        # TODO: save image
        print("COMPLETE: AlphaFold Model")
        # fasta_format is missing first 2 letters like sp/tr but shouldn't matter
        return data["uniprotSequence"], model_path

    # Example of API response


""""[
  {
    "entryId": "AF-P54199-F1",
    "gene": "MPS1",
    "sequenceChecksum": "5A404F4F83A9D548",
    "sequenceVersionDate": "2011-07-27",
    "uniprotAccession": "P54199",
    "uniprotId": "MPS1_YEAST",
    "uniprotDescription": "Serine/threonine-protein kinase MPS1",
    "taxId": 559292,
    "organismScientificName": "Saccharomyces cerevisiae (strain ATCC 204508 / S288c)",
    "uniprotStart": 1,
    "uniprotEnd": 764,
    "uniprotSequence": "MSTNSFHDYVDLKSRTNTRQFSDDEEFTTPPKLSNFGSALLSHTEKTSASEILSSHNNDKIANRLEEMDRSSSRSHPPPSMGNLTSGHTSTSSHSTLFGRYLRNNHQTSMTTMNTSDIEINVGNSLDKSFERIRNLRQNMKEDITAKYAERRSKRFLISNRTTKLGPAKRAMTLTNIFDEDVPNSPNQPINARETVELPLEDSHQTNFKETKRNTDYDSIDFGDLNPIQYIKKHNLPTSDLPLISQIYFDKQREENRQAALRKHSSRELLYKSRSSSSSLSSNNLLANKDNSITSNNGSQPRRKVSTGSSSSKSSIEIRRALKENIDTSNNSNFNSPIHKIYKGISRNKDSDSEKREVLRNISINANHADNLLQQENKRLKRSLDDAITNENINSKNLEVFYHRPAPKPPVTKKVEIVEPAKSASLSNNRNIITVNDSQYEKIELLGRGGSSRVYKVKGSGNRVYALKRVSFDAFDDSSIDGFKGEIELLEKLKDQKRVIQLLDYEMGDGLLYLIMECGDHDLSQILNQRSGMPLDFNFVRFYTKEMLLCIKVVHDAGIVHSDLKPANFVLVKGILKIIDFGIANAVPEHTVNIYRETQIGTPNYMAPEALVAMNYTQNSENQHEGNKWKVGRPSDMWSCGCIIYQMIYGKPPYGSFQGQNRLLAIMNPDVKIPFPEHTSNNEKIPKSAIELMKACLYRNPDKRWTVDKVLSSTFLQPFMISGSIMEDLIRNAVRYGSEKPHISQDDLNDVVDTVLRKFADYKI",
    "modelCreatedDate": "2022-06-01",
    "latestVersion": 4,
    "allVersions": [1, 2, 3, 4],
    "isReviewed": true,
    "isReferenceProteome": true,
    "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-P54199-F1-model_v4.cif",
    "bcifUrl": "https://alphafold.ebi.ac.uk/files/AF-P54199-F1-model_v4.bcif",
    "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-P54199-F1-model_v4.pdb",
    "paeImageUrl": "https://alphafold.ebi.ac.uk/files/AF-P54199-F1-predicted_aligned_error_v4.png",
    "paeDocUrl": "https://alphafold.ebi.ac.uk/files/AF-P54199-F1-predicted_aligned_error_v4.json",
    "amAnnotationsUrl": null,
    "amAnnotationsHg19Url": null,
    "amAnnotationsHg38Url": null
  }
]"""
