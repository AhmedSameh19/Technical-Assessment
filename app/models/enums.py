import enum


class MachineStatus(str, enum.Enum):
    Active = "Active"
    Broken = "Broken"
    Maintenance = "Maintenance"


class WorkOrderStatus(str, enum.Enum):
    Pending = "Pending"
    InProgress = "InProgress"
    Paused = "Paused"
