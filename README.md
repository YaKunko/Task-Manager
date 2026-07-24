# Task Manager

Full-stack task management app: FastAPI + PostgreSQL backend, Vue 3 frontend.

## Features

- Create, view, edit and delete tasks
- Task fields: title, description, status (pending / in progress / completed),
  priority (low / medium / high), deadline, created/updated timestamps
- Filter by status, search by title, sort by creation date or deadline
- Pagination
- Quick status change from the task card
- Loading skeletons, error toasts, empty states
- Swagger / OpenAPI docs
- Unit tests for the API

## Tech Stack

| Layer    | Technology                                              |
|----------|---------------------------------------------------------|
| Backend  | Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic   |
| Database | PostgreSQL 16                                           |
| Frontend | Vue 3, Vite, Pinia, custom CSS                          |
| Infra    | Docker Compose, nginx                                   |
| Tests    | pytest, httpx, aiosqlite                                |

## Quick Start (Docker)

```bash
docker compose up -d --build
```

| Service     | URL                              |
|-------------|----------------------------------|
| Frontend    | http://localhost:8080            |
| API         | http://localhost:8000/api/v1     |
| Swagger UI  | http://localhost:8000/docs       |

Load demo data (15 sample tasks):

```bash
docker compose exec backend python -m app.seed
```

Stop everything:

```bash
docker compose down          # keep database data
docker compose down -v       # remove database data too
```

## Configuration

Copy `.env.example` to `.env` to override defaults (Postgres credentials,
`DATABASE_URL`). The stack works out of the box without a `.env` file.

## API Overview

| Method | Endpoint             | Description                                       |
|--------|----------------------|---------------------------------------------------|
| POST   | `/api/v1/tasks`      | Create a task                                     |
| GET    | `/api/v1/tasks`      | List tasks (filter/search/sort/pagination)        |
| GET    | `/api/v1/tasks/{id}` | Get a single task                                 |
| PATCH  | `/api/v1/tasks/{id}` | Partially update a task (e.g. status only)        |
| DELETE | `/api/v1/tasks/{id}` | Delete a task                                     |

List query parameters: `status`, `search`, `sort_by` (`created_at` | `deadline`),
`sort_order` (`asc` | `desc`), `page`, `page_size` (max 100).

## Local Development

Backend (requires a running Postgres, e.g. `docker compose up -d db`):

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend (dev server proxies `/api` to `localhost:8000`):

```bash
cd frontend
npm install
npm run dev
```

## Running Tests

```bash
cd backend
source .venv/bin/activate
python -m pytest -v
```

Tests run against an in-memory SQLite database — no Docker required.
