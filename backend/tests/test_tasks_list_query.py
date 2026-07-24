async def create_task(client, **overrides):
    payload = {"title": "Task", **overrides}
    response = await client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


async def seed_tasks(client):
    await create_task(client, title="Buy groceries", status="pending")
    await create_task(client, title="Grocery budget review", status="completed")
    await create_task(client, title="Team standup", status="in_progress")
    await create_task(client, title="Deploy release", status="pending")


async def test_filter_by_status(client):
    await seed_tasks(client)
    response = await client.get("/api/v1/tasks", params={"status": "pending"})
    data = response.json()
    assert data["total"] == 2
    assert all(item["status"] == "pending" for item in data["items"])


async def test_filter_by_invalid_status_rejected(client):
    response = await client.get("/api/v1/tasks", params={"status": "bogus"})
    assert response.status_code == 422


async def test_search_by_title_case_insensitive(client):
    await seed_tasks(client)
    response = await client.get("/api/v1/tasks", params={"search": "GROCER"})
    data = response.json()
    assert data["total"] == 2
    titles = {item["title"] for item in data["items"]}
    assert titles == {"Buy groceries", "Grocery budget review"}


async def test_search_and_filter_combined(client):
    await seed_tasks(client)
    response = await client.get(
        "/api/v1/tasks", params={"search": "grocer", "status": "completed"}
    )
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Grocery budget review"


async def test_sort_by_deadline_asc_nulls_last(client):
    await create_task(client, title="No deadline")
    await create_task(client, title="Later", deadline="2026-09-01T00:00:00Z")
    await create_task(client, title="Sooner", deadline="2026-08-01T00:00:00Z")
    response = await client.get(
        "/api/v1/tasks", params={"sort_by": "deadline", "sort_order": "asc"}
    )
    titles = [item["title"] for item in response.json()["items"]]
    assert titles == ["Sooner", "Later", "No deadline"]


async def test_sort_by_invalid_column_rejected(client):
    response = await client.get("/api/v1/tasks", params={"sort_by": "id"})
    assert response.status_code == 422


async def test_pagination_pages_and_slices(client):
    for index in range(5):
        await create_task(client, title=f"Task {index}")
    response = await client.get(
        "/api/v1/tasks",
        params={"page": 2, "page_size": 2, "sort_order": "asc"},
    )
    data = response.json()
    assert data["total"] == 5
    assert data["pages"] == 3
    assert [item["title"] for item in data["items"]] == ["Task 2", "Task 3"]


async def test_page_size_over_limit_rejected(client):
    response = await client.get("/api/v1/tasks", params={"page_size": 101})
    assert response.status_code == 422
