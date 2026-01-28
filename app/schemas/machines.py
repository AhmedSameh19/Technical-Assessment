from pydantic import BaseModel
from app.models import MachineStatus


class MachineStatusUpdate(BaseModel):
    status: MachineStatus
    reason: str | None = None

