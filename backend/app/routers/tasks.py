import math
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_session
from app.models import Task, TaskStatus
from app.schemas import TaskCreate, TaskListResponse, TaskRead, TaskUpdate

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_task_or_404(task_id: int, session: SessionDep) -> Task:
    task = await crud.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, session: SessionDep) -> TaskRead:
    return await crud.create_task(session, data)


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    session: SessionDep,
    status_filter: Annotated[TaskStatus | None, Query(alias="status")] = None,
    search: str | None = None,
    sort_by: Literal["created_at", "deadline"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
) -> TaskListResponse:
    items, total = await crud.list_tasks(
        session,
        status=status_filter,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )
    return TaskListResponse(
        items=[TaskRead.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task: Annotated[Task, Depends(get_task_or_404)]) -> TaskRead:
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    data: TaskUpdate,
    task: Annotated[Task, Depends(get_task_or_404)],
    session: SessionDep,
) -> TaskRead:
    return await crud.update_task(session, task, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: Annotated[Task, Depends(get_task_or_404)],
    session: SessionDep,
) -> None:
    await crud.delete_task(session, task)
