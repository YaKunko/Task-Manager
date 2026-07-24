from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    deadline: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    deadline: datetime | None = None

    @field_validator("title", "status", "priority")
    @classmethod
    def reject_explicit_null(cls, value):
        if value is None:
            raise ValueError("must not be null")
        return value


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    deadline: datetime | None
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    items: list[TaskRead]
    total: int
    page: int
    page_size: int
    pages: int
