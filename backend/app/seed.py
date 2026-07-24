import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.database import SessionLocal
from app.models import Task, TaskPriority, TaskStatus

DEMO_TASKS = [
    ("Set up CI pipeline", "Configure GitHub Actions to run tests on every push.", TaskStatus.in_progress, TaskPriority.high, 2),
    ("Write API documentation", "Document all endpoints with request/response examples.", TaskStatus.pending, TaskPriority.medium, 5),
    ("Fix login redirect bug", "Users land on a blank page after OAuth callback.", TaskStatus.pending, TaskPriority.high, -1),
    ("Refactor user service", "Split the monolithic service module into focused units.", TaskStatus.in_progress, TaskPriority.medium, 7),
    ("Update dependencies", "Bump minor versions and check the changelogs.", TaskStatus.completed, TaskPriority.low, -3),
    ("Design landing page", "Prepare two layout options for review.", TaskStatus.pending, TaskPriority.medium, 10),
    ("Add database indexes", "Cover the slowest queries found in the profiler.", TaskStatus.completed, TaskPriority.high, -5),
    ("Prepare sprint demo", "Collect screenshots and a short script for the demo.", TaskStatus.pending, TaskPriority.medium, 1),
    ("Review pull requests", "Clear the review queue before the code freeze.", TaskStatus.in_progress, TaskPriority.low, None),
    ("Migrate to PostgreSQL 16", "Verify extensions and run the upgrade playbook.", TaskStatus.completed, TaskPriority.high, -10),
    ("Write onboarding guide", "A step-by-step setup guide for new developers.", TaskStatus.pending, TaskPriority.low, None),
    ("Optimize image uploads", "Resize on upload and move originals to cold storage.", TaskStatus.in_progress, TaskPriority.medium, 3),
    ("Clean up feature flags", "Remove flags that have been fully rolled out.", TaskStatus.pending, TaskPriority.low, 14),
    ("Investigate memory leak", "Worker RSS grows steadily under load.", TaskStatus.in_progress, TaskPriority.high, -2),
    ("Plan Q3 roadmap", "Draft goals and staffing for the next quarter.", TaskStatus.pending, TaskPriority.medium, 21),
]


async def seed() -> None:
    async with SessionLocal() as session:
        count = await session.scalar(select(func.count(Task.id)))
        if count:
            print(f"Skipping seed: database already contains {count} tasks.")
            return
        now = datetime.now(timezone.utc)
        for title, description, task_status, priority, deadline_days in DEMO_TASKS:
            deadline = (
                now + timedelta(days=deadline_days)
                if deadline_days is not None
                else None
            )
            session.add(
                Task(
                    title=title,
                    description=description,
                    status=task_status,
                    priority=priority,
                    deadline=deadline,
                )
            )
        await session.commit()
        print(f"Seeded {len(DEMO_TASKS)} demo tasks.")


if __name__ == "__main__":
    asyncio.run(seed())
