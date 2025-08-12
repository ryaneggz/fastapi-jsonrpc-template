## FastAPI JSON-RPC 2.0

Minimal JSON-RPC 2.0 service built with FastAPI.

### Quickstart

```bash
# Create and activate a virtualenv with uv
uv venv
source .venv/bin/activate

# Install dependencies
uv sync

# Start the server (http://localhost:8000)
make run
```

### Test the JSON-RPC endpoint

With the server running, in the same shell (or another shell where the venv is activated):

```bash
python client_example.py
```

This sends a batch request to `http://localhost:8000/rpc` and prints the response, including `ping` and `math.add` results.


