import pytest
from app.kv import KeyValueStore

@pytest.fixture
def kv_store():
    db_file = "test/test.db"
    return KeyValueStore(filename=str(db_file), max_entries=10000)

def test_put_benchmark(benchmark, kv_store):
    benchmark.pedantic(kv_store.put, args=("key", "value"), iterations=1000, rounds=3)

def test_read_benchmark(benchmark, kv_store):
    for i in range(1000):
        kv_store.put(f"key{i}", f"value{i}")
    
    benchmark.pedantic(kv_store.read, args=("key",), iterations=1000, rounds=3)

def test_batch_put_benchmark(benchmark, kv_store):
    keys = [f"key{i}" for i in range(1000)]
    values = [f"value{i}" for i in range(1000)]
    
    benchmark.pedantic(kv_store.batch_put, args=(keys, values), iterations=1000, rounds=1)

# def test_delete_benchmark(benchmark, kv_store):
#     for i in range(1000):
#         kv_store.put(f"key{i}", f"value{i}")
    
#     benchmark.pedantic(kv_store.delete, args=("key",), iterations=1000, rounds=3)


