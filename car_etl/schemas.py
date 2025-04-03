from ninja import Schema
from datetime import datetime
from typing import Optional

class TaskSchema(Schema):
    task_id: str
    is_running: bool
    last_status: Optional[str]
    last_started: Optional[datetime]
    last_finished: Optional[datetime]
    cancel_requested: bool
    next_schedule: Optional[datetime]
    time_next_schedule: Optional[str]
    retry_count: int
    created_at: datetime
    updated_at: datetime
