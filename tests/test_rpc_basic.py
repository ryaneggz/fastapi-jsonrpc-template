def test_ping(client):
    r = client.post("/rpc", json={"jsonrpc":"2.0","method":"ping","id":1})
    assert r.status_code == 200
    assert r.json()["result"] == "pong"

def test_add(client):
    r = client.post("/rpc", json={"jsonrpc":"2.0","method":"math.add","params":{"a":2,"b":3},"id":"x"})
    assert r.json()["result"] == 5

def test_batch(client):
    batch = [
        {"jsonrpc":"2.0","method":"ping","id":1},
        {"jsonrpc":"2.0","method":"nope","id":2},
        {"jsonrpc":"2.0","method":"math.add","params":{"a":1,"b":1}},
    ]
    r = client.post("/rpc", json=batch)
    data = r.json()
    assert len(data) == 2
    ids = {item["id"] for item in data}
    assert ids == {1, 2}
