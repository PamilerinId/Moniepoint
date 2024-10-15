import os
import json
from typing import List

class KeyValueStore:
    """Specify the file based database"""
    # TODO: use a .env before pushing... necessary
    def __init__(self, filename='data/data.db'):
        self.filename = filename
        self.index = {}
        self.load_data()

    def load_data(self):
        """Load existing data from the file into memory."""
        if not os.path.exists(self.filename):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            return

        with open(self.filename, 'r') as f:
            offset = 0
            for line in f:
                data = json.loads(line)
                key = data['key']
                self.index[key] = offset
                offset += len(line)

    def put(self, key: str, value: str):
        """Store a key-value pair."""
        data = json.dumps({'key': key, 'value': value}) + '\n'
        with open(self.filename, 'a') as f:
            f.write(data)
        self.index[key] = os.path.getsize(self.filename) - len(data)

    def read(self, key: str):
        """Retrieve the value associated with a key."""
        if key not in self.index:
            return None

        offset = self.index[key]
        with open(self.filename, 'r') as f:
            f.seek(offset)
            line = f.readline()
            data = json.loads(line)
            return data['value']

    def delete(self, key: str):
        """Mark the key as deleted (set its value to None)."""
        self.put(key, None)

    def batch_put(self, keys: List[str], values: List[str]):
        """Store multiple key-value pairs."""
        for key, value in zip(keys, values):
            self.put(key, value)

    def read_key_range(self, start_key: str, end_key: str):
        """Fetch all key-value pairs within a key range."""
        result = {}
        for key in sorted(self.index.keys()):
            if start_key <= key <= end_key:
                result[key] = self.read(key)
        return result
