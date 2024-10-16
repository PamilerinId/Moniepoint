import os
import json
import mmap
from typing import List, Tuple
from collections import OrderedDict
import threading
import io

""" 
Key-Value Store that implements a simple file-based database with the following operations:
    - put(key, value)
    - read(key)
    - delete(key)
    - batch_put(keys, values)
    - read_key_range(start_key, end_key)
"""
class KeyValueStore:
    def __init__(self, filename='data.db', max_entries=10):
        self.filename = filename
        self.max_entries = max_entries
        self.data = OrderedDict()
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    file_content = f.read().strip()
                    if file_content:
                        loaded_data = json.loads(file_content)
                        self.data = OrderedDict(loaded_data)
                    else:
                        self.data = OrderedDict()
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {self.filename}. Starting with an empty store.")
                self.data = OrderedDict()
        while len(self.data) > self.max_entries:
            self.data.popitem(last=False)

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(list(self.data.items()), f)

    def put(self, key: str, value: str):
        if key in self.data:
            del self.data[key]
        elif len(self.data) >= self.max_entries:
            self.data.popitem(last=False)
        self.data[key] = value
        self.save_data()

    def read(self, key: str):
        if key not in self.data:
            print(f"Key '{key}' not found")
            raise KeyError(f"Key not found")
        return self.data[key]

    def delete(self, key: str):
        if key not in self.data:
            print(f"Key '{key}' not found")
            raise KeyError(f"Key not found")
        del self.data[key]
        self.save_data()

    def batch_put(self, keys: List[str], values: List[str]):
        if len(keys) != len(values):
            raise ValueError("Keys and values must have the same length")
        for key, value in zip(keys, values):
            self.put(key, value)

    def read_key_range(self, start_key: str, end_key: str) -> List[Tuple[str, str]]:
        if start_key > end_key:
            raise ValueError("Start key must be less than or equal to end key")
        return [(k, v) for k, v in self.data.items() if start_key <= k <= end_key]
