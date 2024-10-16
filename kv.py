import os
import json
import mmap
from typing import List, Tuple
from collections import OrderedDict
import threading
import io

class KeyValueStore:
    def __init__(self, filename='data/data.db'):
        self.filename = filename
        self.data = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            # with open(self.filename, 'r') as f:
            #     self.data = json.load(f)
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            return

        with open(self.filename, 'r') as f:
            offset = 0
            for line in f:
                data = json.loads(line)
                key = data['key']
                self.index[key] = offset
                offset += len(line)

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def put(self, key: str, value: str):
        self.data[key] = value
        self.save_data()

    def read(self, key: str):
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found")
        return self.data[key]

    def delete(self, key: str):
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found")
        del self.data[key]
        self.save_data()

    def batch_put(self, keys: List[str], values: List[str]):
        if len(keys) != len(values):
            raise ValueError("Keys and values must have the same length")
        for key, value in zip(keys, values):
            self.data[key] = value
        self.save_data()

    def read_key_range(self, start_key: str, end_key: str) -> List[Tuple[str, str]]:
        if start_key > end_key:
            raise ValueError("Start key must be less than or equal to end key")
        return [(k, v) for k, v in self.data.items() if start_key <= k <= end_key]
