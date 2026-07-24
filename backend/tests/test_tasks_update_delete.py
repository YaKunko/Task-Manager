async def create_task(client, **overrides):
    payload = {"title": "Task", **overrides}
    response = await client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


async def test_patch_title_only_keeps_other_fields(client):
    created = await create_task(
        client, title="Original", description="Keep me", priority="high"
    )
    response = await client.patch(
        f"/api/v1/tasks/{created['id']}", json={"title": "Renamed"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Renamed"
    assert data["description"] == "Keep me"
    assert data["priority"] == "high"


async def test_patch_status_only(client):
    created = await create_task(client)
    response = await client.patch(
        f"/api/v1/tasks/{created['id']}", json={"status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


async def test_patch_can_clear_deadline(client):
    created = await create_task(client, deadline="2026-08-01T00:00:00Z")
    response = await client.patch(
        f"/api/v1/tasks/{created['id']}", json={"deadline": None}
    )
    assert response.status_code == 200
    assert response.json()["deadline"] is None


async def test_patch_missing_task_returns_404(client):
    response = await client.patch("/api/v1/tasks/999", json={"title": "Nope"})
    assert response.status_code == 404


async def test_patch_invalid_status_rejected(client):
    created = await create_task(client)
    response = await client.patch(
        f"/api/v1/tasks/{created['id']}", json={"status": "done"}
    )
    assert response.status_code == 422


async def test_delete_task(client):
    created = await create_task(client)
    response = await client.delete(f"/api/v1/tasks/{created['id']}")
    assert response.status_code == 204
    follow_up = await client.get(f"/api/v1/tasks/{created['id']}")
    assert follow_up.status_code == 404


async def test_delete_missing_task_returns_404(client):
    response = await client.delete("/api/v1/tasks/999")
    assert response.status_code == 404
