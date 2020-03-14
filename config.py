import json
import os

def getConfig():
    # Set-up config
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'config/config.json')
    with open(file_path) as config_file:
        config = json.loads(config_file.read())
    return config