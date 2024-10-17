# Key-Value Store API

This project implements a simple key-value store API using FastAPI and Python.

## Setup

1. Ensure you have Python 3.11 installed on your system.

2. Clone this repository:
   ```
   git clone `https://github.com/PamilerinId/moniepoint-assessment.git`
   cd moniepoint-assessment
   ```

3. Install dependencies using Pipenv:
   ```
   pip install pipenv
   pipenv install
   ```

## Running the API

1. Activate the virtual environment:
   ```
   pipenv shell
   ```

2. Start the FastAPI server:
   ```
   uvicorn app.main:app --port=8003 --reload 
   ```

   The API will be available at `http://localhost:8003/docs`.

## API Endpoints

- `GET /read/{key}`: Retrieve a value for a given key
- `GET /read_key_range/`: Fetch key-value pairs in a specified range
- `POST /put/`: Store a key-value pair
- `POST /batch_put/`: Store multiple key-value pairs
- `DELETE /delete/{key}`: Delete a key-value pair

## Running Tests

To run the tests, use the following command:
```
pytest test/test_kv.py    --- All tests pass ✔️
pytest test/test_main.py  --- All tests pass 6️⃣
```

## Running Benchmarks

To run the benchmarks, use the following command:
```
pytest test/test_benchmarks.py
```   
### Notes
- I set the max_entries to 10000, and ran the benchmarks 3 times for each operation in an attempt to simulate a heavy load on the server.
- The batch_put was only run once as it took too long to run.
- The read operation was the fastest, followed by the put operation(obviously).


