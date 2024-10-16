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
    
    try:
        value = kv_store.read(key)
    except KeyError:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": "Key data fetched successfully.", "data": {"key": key, "value": value}}


@app.get("/read_key_range/")
def read_key_range(start_key: str, end_key: str):
    """Fetch key-value pairs in the specified key range."""
    try:
        result = kv_store.read_key_range(start_key, end_key)
    except KeyError:
        raise HTTPException(status_code=404, detail="Key range not found")
    return {"message": "Data range fetched successfully.", "data": result}


@app.post("/put/")
def put(key: str, value: str):
    """Store a key-value pair."""
    try:
        kv_store.put(key, value)
    except KeyError:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": "Key-Value pair stored successfully.", "data": {"key": key, "value": value}}

@app.post("/batch_put/")
def batch_put(keys: List[str], values: List[str]):
    """Store multiple key-value pairs."""
    if len(keys) != len(values):
        raise HTTPException(status_code=400, detail="Keys and values length must match")
    try:
        kv_store.batch_put(keys, values)
    except KeyError:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": "Batch put successful.", "data": {"keys": keys, "values": values}}


@app.delete("/delete/{key}")
def delete(key: str):
    """Delete a key-value pair."""
    try:
        kv_store.delete(key)
    except KeyError:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": "Key deleted successfully.", "data": {"key": key}}