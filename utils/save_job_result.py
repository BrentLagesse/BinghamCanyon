from pathlib import Path
import json
from datetime import datetime
from constants import RESULT_NAME


# For time sake I didn't make an interface but 100% should
# TODO:Make an interface and use constructor to pass in results.
def save_job_result(
    method: int,
    output_path: Path,
    sss_uniprot_url: str,
    model_path: Path,
    protein_uniprot_entry: str,
    jalview_url: str,
    start_time: datetime,
    end_time,
):
    """Creates job config for in output_folder
    Args:
        method (int): number corresponds with ones in docs
        settings (dict) :
    """
    data = dict(
        method=method,
        sss_uniprot_url=sss_uniprot_url,
        model_path=str(model_path),
        protein_uniprot_entry=protein_uniprot_entry,
        jalview_url=jalview_url,
        start_time=str(start_time),
        end_time=str(end_time),
    )

    print(str(data))
    json_path = output_path / RESULT_NAME
    with json_path.open("w") as json_file:
        json.dump(data, json_file, indent=2)
