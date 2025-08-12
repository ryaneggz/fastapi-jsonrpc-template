import httpx

URL = "http://localhost:8000/rpc"
batch = [
    {"jsonrpc":"2.0","method":"ping","id":1},
    {"jsonrpc":"2.0","method":"math.add","params":{"a":40,"b":2},"id":2},
    {"jsonrpc":"2.0","method":"ping"}  # notification
]
print(httpx.post(URL, json=batch).json())
