from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_existing_key():
    response = client.post("/put/", params={"key": "test_key", "value": "test_value"})
    assert response.status_code == 200

    response = client.get("/read/test_key")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Key data fetched successfully.",
        "data": {"key": "test_key", "value": "test_value"}
    }

def test_read_non_existing_key():
    response = client.get("/read/non_existing_key")
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found"}

def test_read_key_range():
    client.post("/put/", params={"key": "a", "value": "1"})
    client.post("/put/", params={"key": "b", "value": "2"})
    client.post("/put/", params={"key": "c", "value": "3"})

    response = client.get("/read_key_range/", params={"start_key": "a", "end_key": "c"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Data range fetched successfully.",
        "data": [{"key": "a", "value": "1"}, {"key": "b", "value": "2"}, {"key": "c", "value": "3"}]
    }

def test_put():
    response = client.post("/put/", params={"key": "new_key", "value": "new_value"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Key-Value pair stored successfully.",
        "data": {"key": "new_key", "value": "new_value"}
    }

    # Verify the key was actually stored
    response = client.get("/read/new_key")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Key data fetched successfully.",
        "data": {"key": "new_key", "value": "new_value"}
    }

def test_batch_put():
    keys = ["key1", "key2", "key3"]
    values = ["value1", "value2", "value3"]
    response = client.post("/batch_put/", json={"keys": keys, "values": values})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Batch put successful.",
        "data": {"keys": keys, "values": values}
    }

    # Verify the keys were actually stored
    for key, value in zip(keys, values):
        response = client.get(f"/read/{key}")
        assert response.status_code == 200
        assert response.json() == {
            "message": "Key data fetched successfully.",
            "data": {"key": key, "value": value}
        }

def test_batch_put_unequal_lists():
    keys = ["key1", "key2"]
    values = ["value1"]
    response = client.post("/batch_put/", json={"keys": keys, "values": values})
    assert response.status_code == 400
    assert response.json() == {"detail": "Keys and values length must match"}

def test_delete():
    # First, let's add a key-value pair
    client.post("/put/", params={"key": "delete_me", "value": "temp_value"})

    # Now, let's delete it
    response = client.delete("/delete/delete_me")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Key deleted successfully.",
        "data": {"key": "delete_me"}
    }

    # Verify the key was actually deleted
    response = client.get("/read/delete_me")
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found"}
