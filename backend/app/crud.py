from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task, TaskStatus
from app.schemas import TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    return await session.get(Task, task_id)


async def list_tasks(
    session: AsyncSession,
    *,
    status: TaskStatus | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[Task], int]:
    query = select(Task)
    if status is not None:
        query = query.where(Task.status == status)
    if search:
        query = query.where(Task.title.ilike(f"%{search}%"))

    total = await session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    sort_column = getattr(Task, sort_by)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc().nulls_last(), Task.id.desc())
    else:
        query = query.order_by(sort_column.asc().nulls_last(), Task.id.asc())

    query = query.offset((page - 1) * page_size).limit(page_size)
    items = (await session.scalars(query)).all()
    return list(items), total or 0


async def update_task(session: AsyncSession, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task: Task) -> None:
    await session.delete(task)
    await session.commit()
