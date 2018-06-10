import os
import json

env = os.environ.get('PYTHON_ENV', 'development')

path = os.path.dirname(os.path.abspath(__file__))


def get_config():
    config = open(path + '/db_config.json').read()
    env_config = json.loads(config)[env]
    return env_config
