async def create_task(client, **overrides):
    payload = {"title": "Task", **overrides}
    response = await client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


async def test_get_task_by_id(client):
    created = await create_task(client, title="Find me")
    response = await client.get(f"/api/v1/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


async def test_get_missing_task_returns_404(client):
    response = await client.get("/api/v1/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


async def test_list_returns_pagination_envelope(client):
    await create_task(client, title="A")
    await create_task(client, title="B")
    response = await client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["pages"] == 1
    assert len(data["items"]) == 2


async def test_list_default_sort_is_created_at_desc(client):
    first = await create_task(client, title="First")
    second = await create_task(client, title="Second")
    response = await client.get("/api/v1/tasks")
    ids = [item["id"] for item in response.json()["items"]]
    assert ids == [second["id"], first["id"]]


async def test_empty_list(client):
    response = await client.get("/api/v1/tasks")
    data = response.json()
    assert data == {"items": [], "total": 0, "page": 1, "page_size": 10, "pages": 0}
