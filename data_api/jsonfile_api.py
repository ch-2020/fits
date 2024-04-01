import os, json

class JsonFileApi:
    def __init__(self, file_path: str) -> None:
        self.file_path = ""
        self.file_exist = False
        self.json = {}

        if os.path.isfile(file_path):
            self.file_exist = True
            self.file_path = file_path
        else:
            print("Error while reading file!")
        
    def extract_data(self) -> dict:
        if self.file_exist:
            with open(self.file_path, "r") as f:
                return json.load(f)
        else:
            return {}