import pytest
import os
from kv import KeyValueStore

@pytest.fixture
def kv_store():
    return KeyValueStore()

def test_put_and_read(kv_store):
    kv_store.put("test_key", "test_value")
    assert kv_store.read("test_key") == "test_value"

def test_read_non_existent_key(kv_store):
    with pytest.raises(KeyError):
        kv_store.read("non_existent_key")

def test_delete(kv_store):
    kv_store.put("delete_me", "temp_value")
    assert kv_store.read("delete_me") == "temp_value"
    
    kv_store.delete("delete_me")
    with pytest.raises(KeyError):
        kv_store.read("delete_me")

def test_delete_non_existent_key(kv_store):
    with pytest.raises(KeyError):
        kv_store.delete("non_existent_key")

def test_batch_put(kv_store):
    keys = ["key1", "key2", "key3"]
    values = ["value1", "value2", "value3"]
    kv_store.batch_put(keys, values)
    
    for key, value in zip(keys, values):
        assert kv_store.read(key) == value

def test_batch_put_large(kv_store):
    keys = [f"key{i}" for i in range(20)]
    values = [f"value{i}" for i in range(20)]
    kv_store.batch_put(keys, values)
    
    # Check that only the last 10 keys are in the index
    for i in range(10):
        with pytest.raises(KeyError):
            kv_store.read(f"key{i}")
    
    for i in range(10, 20):
        assert kv_store.read(f"key{i}") == f"value{i}"

def test_batch_put_unequal_lists(kv_store):
    keys = ["key1", "key2"]
    values = ["value1"]
    with pytest.raises(ValueError):
        kv_store.batch_put(keys, values)

def test_read_key_range(kv_store):
    kv_store.put("a", "1")
    kv_store.put("b", "2")
    kv_store.put("c", "3")
    kv_store.put("d", "4")

    result = kv_store.read_key_range("b", "d")
    assert result == [("b", "2"), ("c", "3"), ("d", "4")]

def test_read_key_range_empty(kv_store):
    result = kv_store.read_key_range("x", "z")
    assert result == []

def test_read_key_range_invalid(kv_store):
    kv_store.put("a", "1")
    kv_store.put("c", "3")

    with pytest.raises(ValueError):
        kv_store.read_key_range("c", "a")

def test_index_size_limit(kv_store):
    for i in range(15):
        kv_store.put(f"key{i}", f"value{i}")
    
    # The index size is set to 10, so the first 5 keys should be removed from the index
    with pytest.raises(KeyError):
        kv_store.read("key0")
    
    # The last 10 keys should still be in the index
    for i in range(5, 15):
        assert kv_store.read(f"key{i}") == f"value{i}"

def test_persistence(tmp_path):
    db_file = tmp_path / "persist_test.db"
    kv_store1 = KeyValueStore(filename=str(db_file))
    
    kv_store1.put("persist_key", "persist_value")
    
    # Create a new instance with the same file
    kv_store2 = KeyValueStore(filename=str(db_file))
    
    assert kv_store2.read("persist_key") == "persist_value"
