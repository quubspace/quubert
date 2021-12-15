import lightbulb

from pathlib import Path


def extensions():
    files = Path("app", "extensions").rglob("*.py")
    for file in files:
        yield file.as_posix()[:-3].replace("/", ".")


def load_extensions(_bot):
    for ext in extensions():
        try:
            _bot.load_extensions(ext)
        except Exception as ex:
            print(f"Failed to load extension {ext} - exception: {ex}")


class Bot:
    def __init__(
        self, app: lightbulb.BotApp, user_data: dict, py_version: str, version: str
    ):
        self.app = app
        self.user_data = user_data
        self.py_version = py_version
        self.version = version

    def run(self):
        load_extensions(self.app)
        self.app.run()
