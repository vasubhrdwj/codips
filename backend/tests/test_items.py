def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_read_item(client):
    # Create
    res = client.post("/api/v1/items/", json={"name": "Widget", "description": "A fine widget"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Widget"
    item_id = data["id"]

    # Read
    res = client.get(f"/api/v1/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["id"] == item_id


def test_update_item(client):
    res = client.post("/api/v1/items/", json={"name": "Old"})
    item_id = res.json()["id"]
    res = client.patch(f"/api/v1/items/{item_id}", json={"name": "New"})
    assert res.status_code == 200
    assert res.json()["name"] == "New"


def test_delete_item(client):
    res = client.post("/api/v1/items/", json={"name": "ToDelete"})
    item_id = res.json()["id"]
    res = client.delete(f"/api/v1/items/{item_id}")
    assert res.status_code == 204
    res = client.get(f"/api/v1/items/{item_id}")
    assert res.status_code == 404
