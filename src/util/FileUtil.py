import sys
import json


class FileUtil:

    @staticmethod
    def load_config_file():
        try:
            file = open("../config.json")
        except FileNotFoundError:
            print("No 'config.json' file was found in the root of the repository. "
                  "Working directory of the script is intended to be the 'src'-directory.")
            sys.exit()
        try:
            # noinspection PyUnboundLocalVariable
            config = json.load(file)
        except json.decoder.JSONDecodeError:
            print("Syntax issues found in the config.json file.")
            sys.exit()
        return config
