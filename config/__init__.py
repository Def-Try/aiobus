import json

with open("config/token.txt", 'r') as f:
    TOKEN = f.readlines()[0]

with open("config/config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())
