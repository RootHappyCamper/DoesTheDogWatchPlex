import yaml
import sys
import os

parent_directory = os.path.abspath('..')
sys.path.append(parent_directory)

def load_config_yaml():
    with open("config.yml", 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data