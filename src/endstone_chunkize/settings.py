import os
import tomllib

DEFAULT_CONFIG = """[generation]
cellChunks = 8
maxActiveAreas = 4
checkIntervalTicks = 10
cellTimeoutSeconds = 60
settleSeconds = 20
stampChunks = true
maxRadius = 50000

[progress]
autoResume = true
logIntervalSeconds = 30
saveIntervalSeconds = 30
"""


def clamp(value, low, high):
    return max(low, min(high, value))


class Settings:
    def __init__(self, dataFolder):
        path = os.path.join(dataFolder, "config.toml")
        os.makedirs(dataFolder, exist_ok=True)
        if not os.path.isfile(path):
            with open(path, "w", encoding="utf-8") as file:
                file.write(DEFAULT_CONFIG)
        try:
            with open(path, "rb") as file:
                raw = tomllib.load(file)
        except (OSError, tomllib.TOMLDecodeError):
            raw = {}
        generation = raw.get("generation", {})
        progress = raw.get("progress", {})
        self.cellChunks = clamp(int(generation.get("cellChunks", 8)), 1, 10)
        self.maxActiveAreas = clamp(int(generation.get("maxActiveAreas", 4)), 1, 10)
        self.checkIntervalTicks = clamp(int(generation.get("checkIntervalTicks", 10)), 1, 200)
        self.cellTimeoutSeconds = clamp(int(generation.get("cellTimeoutSeconds", 60)), 5, 3600)
        self.settleSeconds = clamp(int(generation.get("settleSeconds", 20)), 0, 600)
        self.stampChunks = bool(generation.get("stampChunks", True))
        self.maxRadius = clamp(int(generation.get("maxRadius", 50000)), 16, 1000000)
        self.autoResume = bool(progress.get("autoResume", True))
        self.logIntervalSeconds = clamp(int(progress.get("logIntervalSeconds", 30)), 0, 3600)
        self.saveIntervalSeconds = clamp(int(progress.get("saveIntervalSeconds", 30)), 5, 3600)
