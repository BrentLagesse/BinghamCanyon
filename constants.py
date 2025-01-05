from typing import Final
from pathlib import Path

# Constants used throughout the app so can easily change them
# Final doesn't actually prevent reassignment when running but your IDE should throw an error when you do
# For VSCODE users, put this in your setting.json
# {
#   "python.analysis.typeCheckingMode": "basic"
# }
# TODO: Go through the code and put shared hard coded variables to constants
OUTPUT_FOLDER_PATH: Final[Path] = Path("output")
ALIGNED_SEQUENCE_NAME: Final[str] = "aligned_sequence.aln"
CONFIG_NAME: Final[str] = "config.json"
RESULT_NAME: Final[str] = "result.json"
