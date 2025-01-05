import json
from typing import TypedDict
from pathlib import Path
from constants import CONFIG_NAME

# TODO: Adding typing
# Python it is really hard to add typing
# class ChimeraXType(TypedDict):
#     exe_path : str
# class JalviewType(TypedDict):
#     exe_path : str

# class SequenceDatabaseType(TypedDict):
#     is_individually_retrieved : bool
# class SequenceSimilarlySearchParse(TypedDict):
#     target_match : int
#     max_entries : int
# class SequenceSimilarlySearch(TypedDict):
#     check_delay : int
#     parse : SequenceSimilarlySearchParse
# class JalviewType(TypedDict):

# class ConfigType(TypedDict):
#     input_mode : bool
#     output_folder_path : str
#     chimerax : ChimeraXType
#     jalview : JalviewType
#     sequence_database : SequenceDatabaseType


# Reads config.json
# TODO:
# Modified version of  https://stackoverflow.com/questions/19078170/how-would-you-save-a-simple-settings-configuration-file-in-python


class Dict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config(object):
    # TODO: Change to use pathlib
    @staticmethod
    def __load__(data):
        if type(data) is dict:
            return Config.load_dict(data)
        elif type(data) is list:
            return Config.load_list(data)
        else:
            return data

    @staticmethod
    def load_dict(data: dict):
        result = Dict()
        for key, value in data.items():
            result[key] = Config.__load__(value)
        return result

    @staticmethod
    def load_list(data: list):
        result = [Config.__load__(item) for item in data]
        return result

    @staticmethod
    def load_json(path: str):
        with open(path, "r") as f:
            result = Config.__load__(json.loads(f.read()))
        return result


class ConfigManager:
    """
    Wrapper class for Config
    """

    # Holds Config what it returns
    conf: Config

    def __init__(self, config_path: Path):
        self.conf = Config.load_json(str(config_path))

    def reset(self):
        config_default = Config.load_json("config-default.json")
        print("Inside config:" + str(self.conf))
        jsonpath = Path("config" + ".json")
        jsonpath.write_text(json.dumps(config_default, indent=2))
        self.conf = config_default

    def save(self, output_path: Path = Path()):
        """
        Args:
            output_path (Path, optional): default is saves to root of project. specifying path means it is save there instead
        """
        jsonpath = output_path / CONFIG_NAME
        jsonpath.write_text(json.dumps(self.conf, indent=2))
