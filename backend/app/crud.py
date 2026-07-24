from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from app.schemas import TaskCreate


async def create_task(session: AsyncSession, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
