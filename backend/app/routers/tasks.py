from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_session
from app.schemas import TaskCreate, TaskRead

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate, session: SessionDep) -> TaskRead:
    return await crud.create_task(session, data)
