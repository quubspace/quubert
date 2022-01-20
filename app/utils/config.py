import json
import os

default_config = {
    "token": "",
    "sender_email": "",
    "smtp_host": "",
    "email_port": "",
    "email_password": "",
    "receiver_email": "",
    "next_check": "0",
    "database": "",
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

        self.token = self.config.get("token", default_config.get("token"))
        self.sender_email = self.config.get(
            "sender_email", default_config.get("sender_email")
        )
        self.smtp_host = self.config.get("smtp_host", default_config.get("smtp_host"))
        self.email_port = self.config.get(
            "email_port", default_config.get("email_port")
        )
        self.email_password = self.config.get(
            "email_password", default_config.get("email_password")
        )
        self.receiver_email = self.config.get(
            "receiver_email", default_config.get("receiver_email")
        )
        self.next_check = self.config.get(
            "next_check", default_config.get("next_check")
        )
        self.database = self.config.get("database", default_config.get("database"))

    def store(self):
        c = {
            "token": self.token,
            "sender_email": self.sender_email,
            "smtp_host": self.smtp_host,
            "email_port": self.email_port,
            "email_password": self.email_password,
            "receiver_email": self.receiver_email,
            "next_check": self.next_check,
            "database": self.database,
        }

        with open(self.filename, "w") as file:
            json.dump(c, file)
