import json
import os

default_config = {
    "database": "",
    "email": "",
}


class Config:
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.config = {}
        if not os.path.isfile(filename):
            with open(filename, "w") as file:
                json.dump(default_config, file)
        with open(filename) as file:
            self.config = json.load(file)
        self.email = self.config.get("email", default_config.get("email"))
        self.database = self.config.get("database", default_config.get("database"))

    def store(self):
        c = {
            "email": self.email,
            "database": self.database,
        }
        with open(self.filename, "w") as file:
            json.dump(c, file)
