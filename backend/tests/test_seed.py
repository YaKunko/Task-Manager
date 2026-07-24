from app.models import TaskPriority, TaskStatus
from app.seed import DEMO_TASKS


def test_demo_tasks_are_varied():
    assert len(DEMO_TASKS) == 15
    statuses = {entry[2] for entry in DEMO_TASKS}
    priorities = {entry[3] for entry in DEMO_TASKS}
    deadline_days = [entry[4] for entry in DEMO_TASKS]
    assert statuses == set(TaskStatus)
    assert priorities == set(TaskPriority)
    assert any(days is None for days in deadline_days)
    assert any(days is not None and days < 0 for days in deadline_days)
