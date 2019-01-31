import json
import os

import numpy as np


class NumpyEncoder(json.JSONEncoder):
    # Encodes numpy arrays as lists since JSON does not support np.ndarray
    def default(self, obj):
        return obj.tolist() if isinstance(obj, np.ndarray) else json.JSONEncoder.default(self, obj)


class Configuration(object):
    DEFAULT_CONFIGURATION_FILE_PATH = os.path.join(os.getcwd(), 'vision/config/default_configuration.json')
    CONFIGURATION_FILE_PATH = os.path.join(os.getcwd(), 'vision/config/configuration.json')

    def __init__(self):
        self.config = None

    def load(self):
        # Load the configuration JSON file
        file_path = self.CONFIGURATION_FILE_PATH \
            if os.path.isfile(self.CONFIGURATION_FILE_PATH) else self.DEFAULT_CONFIGURATION_FILE_PATH
        with open(file_path, 'r') as fp:
            self.config = json.load(fp)

        return self.config

    def save(self):
        # Save the configurations in a JSON file
        with open(self.CONFIGURATION_FILE_PATH, 'w') as fp:
            json.dump(self.config, fp, sort_keys=True, indent=2, cls=NumpyEncoder)

    def update(self, field, value):
        # Update a value in the configuration
        self.config[field] = value
        self.save()
