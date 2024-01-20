import json

with open("config/token.txt", "r", encoding="utf-8") as f:
    TOKEN = f.readlines()[0]

with open("config/config.cfg", "r", encoding="utf-8") as f:
    CONFIG = json.loads(f.read())
