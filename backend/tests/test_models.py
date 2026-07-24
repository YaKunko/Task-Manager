from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Task, TaskPriority, TaskStatus


async def test_task_defaults():
    engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        task = Task(title="Sample task")
        session.add(task)
        await session.commit()
        await session.refresh(task)

    assert task.id == 1
    assert task.status == TaskStatus.pending
    assert task.priority == TaskPriority.medium
    assert task.description is None
    assert task.deadline is None
    assert task.created_at is not None
    assert task.updated_at is not None
    await engine.dispose()
