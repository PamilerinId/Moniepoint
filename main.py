from fastapi import FastAPI, HTTPException
from typing import List
from kv import KeyValueStore

app = FastAPI(
    title="Moniepoint | KV DB Assessment",
    description="A Key/Value DB system to simulate Redis/DB Operations",
    version="1.0.0",
)
kv_store = KeyValueStore()


@app.get("/read/{key}")
def read(key: str):
    """Retrieve the value for a given key."""
    value = kv_store.read(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}


@app.get("/read_key_range/")
def read_key_range(start_key: str, end_key: str):
    """Fetch key-value pairs in the specified key range."""
    result = kv_store.read_key_range(start_key, end_key)
    return {"range": result}


@app.post("/put/")
def put(key: str, value: str):
    """Store a key-value pair."""
    kv_store.put(key, value)
    return {"message": "Key-Value pair stored successfully."}

@app.post("/batch_put/")
def batch_put(keys: List[str], values: List[str]):
    """Store multiple key-value pairs."""
    if len(keys) != len(values):
        raise HTTPException(status_code=400, detail="Keys and values length must match")
    kv_store.batch_put(keys, values)
    return {"message": "Batch put successful."}


@app.delete("/delete/{key}")
def delete(key: str):
    """Delete a key-value pair."""
    kv_store.delete(key)
    return {"message": "Key deleted successfully."}