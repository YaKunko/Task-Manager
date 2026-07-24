async def test_create_task_returns_201_with_fields(client):
    payload = {
        "title": "Write report",
        "description": "Quarterly report for the team",
        "status": "in_progress",
        "priority": "high",
        "deadline": "2026-08-01T12:00:00Z",
    }
    response = await client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Write report"
    assert data["description"] == "Quarterly report for the team"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"
    assert data["deadline"] is not None
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


async def test_create_task_minimal_uses_defaults(client):
    response = await client.post("/api/v1/tasks", json={"title": "Minimal"})
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["priority"] == "medium"
    assert data["description"] is None
    assert data["deadline"] is None


async def test_create_task_empty_title_rejected(client):
    response = await client.post("/api/v1/tasks", json={"title": ""})
    assert response.status_code == 422


async def test_create_task_too_long_title_rejected(client):
    response = await client.post("/api/v1/tasks", json={"title": "x" * 201})
    assert response.status_code == 422


async def test_create_task_invalid_status_rejected(client):
    response = await client.post(
        "/api/v1/tasks", json={"title": "Valid", "status": "done"}
    )
    assert response.status_code == 422
