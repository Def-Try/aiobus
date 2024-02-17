import json

with open("config/tokens.json", "r", encoding="utf-8") as f:
    TOKENS = json.loads(f.read())

with open("config/config.cfg", "r", encoding="utf-8") as f:
    CONFIG = json.loads(f.read())
